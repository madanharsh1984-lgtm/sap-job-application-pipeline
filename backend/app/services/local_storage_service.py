from __future__ import annotations

import base64
import hashlib
import hmac
import json
import logging
import os
import re
import time
import urllib.parse
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

logger = logging.getLogger(__name__)

DEFAULT_LOCAL_DATA_DIR = r"C:\Users\madan\OneDrive\Desktop\Linkdin Job\data"
MAX_KEYWORDS = 30
DEFAULT_APIFY_ACTOR_ID = 'harvestapi~linkedin-post-search'
FREE_JOB_LIMIT = 5
DEFAULT_PLAN = 'basic'
DEFAULT_PLAN_PRICE_INR = 499


@dataclass
class LocalDataPaths:
    root: Path
    jobs: Path
    logs: Path
    resumes: Path
    keywords: Path
    users_json: Path
    system_log: Path


def get_local_data_paths() -> LocalDataPaths:
    root = Path(os.getenv('LOCAL_DATA_DIR', DEFAULT_LOCAL_DATA_DIR))
    paths = LocalDataPaths(
        root=root,
        jobs=root / 'jobs',
        logs=root / 'logs',
        resumes=root / 'resumes',
        keywords=root / 'keywords',
        users_json=root / 'users.json',
        system_log=root / 'logs' / 'system.log',
    )
    for item in (paths.root, paths.jobs, paths.logs, paths.resumes, paths.keywords):
        item.mkdir(parents=True, exist_ok=True)
    if not paths.users_json.exists():
        paths.users_json.write_text('[]\n', encoding='utf-8')
    return paths


def _log(paths: LocalDataPaths, level: str, message: str) -> None:
    timestamp = datetime.now(timezone.utc).isoformat()
    line = f'{timestamp} | {level.upper()} | {message}\n'
    with paths.system_log.open('a', encoding='utf-8') as fh:
        fh.write(line)


def normalize_keywords(keywords: list[str]) -> list[str]:
    normalized: set[str] = set()
    for keyword in keywords:
        stripped = keyword.strip(".,;:!?()[]{}\"' ").lower()
        if stripped:
            normalized.add(stripped)
    return sorted(normalized)


def extract_keywords(resume_content: str) -> list[str]:
    tokens = re.findall(r"[A-Za-z0-9+#./-]+", resume_content or '')
    candidates = [token for token in tokens if len(token) > 4]
    return normalize_keywords(candidates)[:MAX_KEYWORDS]


def keyword_set_id(normalized_keywords: list[str]) -> str:
    return hashlib.sha256('|'.join(normalized_keywords).encode('utf-8')).hexdigest()[:16]


def _load_users(paths: LocalDataPaths) -> list[dict]:
    try:
        data = json.loads(paths.users_json.read_text(encoding='utf-8'))
        if isinstance(data, list):
            return data
    except (OSError, json.JSONDecodeError) as exc:
        logger.warning('Could not load users.json: %s', exc)
    return []


def _save_users(paths: LocalDataPaths, users: list[dict]) -> None:
    paths.users_json.write_text(json.dumps(users, indent=2, ensure_ascii=False), encoding='utf-8')


def _safe_email(email: str) -> str:
    return email.replace('@', '_at_').replace('.', '_')


def _save_keywords(paths: LocalDataPaths, email: str, keywords: list[str], ks_id: str) -> None:
    file = paths.keywords / f'{_safe_email(email)}.json'
    payload = {
        'email': email,
        'keyword_set_id': ks_id,
        'keywords': keywords,
        'saved_at': datetime.now(timezone.utc).isoformat(),
    }
    file.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding='utf-8')


def _save_resume(paths: LocalDataPaths, email: str, resume_content: str) -> str:
    file = paths.resumes / f'{_safe_email(email)}.txt'
    file.write_text(resume_content, encoding='utf-8')
    return str(file)


def _load_job_payload(file: Path) -> dict:
    payload = json.loads(file.read_text(encoding='utf-8'))
    return payload if isinstance(payload, dict) else {}


def _enrich_user(user: dict) -> dict:
    enriched = dict(user)
    enriched.setdefault('subscription_status', 'FREE')
    enriched.setdefault('payment_id', '')
    enriched.setdefault('plan', DEFAULT_PLAN)
    enriched.setdefault('plan_amount', DEFAULT_PLAN_PRICE_INR)
    return enriched


def _find_user(users: list[dict], email: str) -> dict | None:
    user = next((item for item in users if isinstance(item, dict) and item.get('email') == email), None)
    return _enrich_user(user) if user else None


def _local_fallback_jobs(keywords: list[str]) -> list[dict]:
    top = keywords[:5] or ['sap consultant']
    now = datetime.now(timezone.utc).isoformat()
    jobs: list[dict] = []
    for index, keyword in enumerate(top, start=1):
        jobs.append(
            {
                'id': f'local-{index}',
                'title': f'{keyword.title()} Role',
                'company': f'Company {index}',
                'location': 'Remote',
                'url': f'https://example.local/jobs/{index}',
                'posted_at': now,
                'content': f'Local generated job for keyword: {keyword}',
                'source': 'local',
            }
        )
    return jobs


def _apify_request(token: str, method: str, path: str, body: dict | None = None) -> tuple[int, dict | list]:
    url = f'https://api.apify.com/v2{path}'
    payload = json.dumps(body).encode('utf-8') if body is not None else None
    req = urllib.request.Request(url, data=payload, method=method)
    req.add_header('Authorization', f'Bearer {token}')
    req.add_header('Content-Type', 'application/json')
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            raw = response.read().decode('utf-8')
            return response.status, json.loads(raw) if raw.strip() else {}
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode('utf-8', errors='ignore')
        return exc.code, {'error': raw[:1000]}
    except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError) as exc:
        return 0, {'error': str(exc)}


def _scrape_jobs_from_apify(keywords: list[str]) -> list[dict]:
    token = os.getenv('APIFY_TOKEN', '').strip()
    if not token:
        raise RuntimeError('APIFY_TOKEN is not configured')

    actor_id = os.getenv('APIFY_ACTOR_ID', DEFAULT_APIFY_ACTOR_ID).strip() or DEFAULT_APIFY_ACTOR_ID
    status, run_response = _apify_request(
        token,
        'POST',
        f'/acts/{actor_id}/runs',
        body={
            'searchQueries': keywords[:8],
            'maxPosts': int(os.getenv('APIFY_MAX_POSTS', '50')),
            'sort': 'date',
            'scrapeReactions': False,
            'scrapeComments': False,
        },
    )
    if status not in (200, 201):
        raise RuntimeError(f'Failed to start Apify actor: status={status}')

    run_id = (run_response or {}).get('data', {}).get('id')
    if not run_id:
        raise RuntimeError('Apify run ID missing')

    dataset_id = ''
    for _ in range(45):
        time.sleep(2)
        run_status_code, run_status_response = _apify_request(token, 'GET', f'/actor-runs/{run_id}')
        if run_status_code != 200:
            continue
        run_data = (run_status_response or {}).get('data', {})
        run_state = run_data.get('status')
        if run_state == 'SUCCEEDED':
            dataset_id = run_data.get('defaultDatasetId', '')
            break
        if run_state in ('FAILED', 'ABORTED', 'TIMED-OUT'):
            raise RuntimeError(f'Apify run failed with state={run_state}')
    if not dataset_id:
        raise RuntimeError('Apify run timeout')

    dataset_status, dataset_response = _apify_request(
        token,
        'GET',
        f'/datasets/{dataset_id}/items?clean=true&format=json&limit=1000',
    )
    if dataset_status != 200:
        raise RuntimeError(f'Failed to fetch Apify dataset: status={dataset_status}')

    records = dataset_response if isinstance(dataset_response, list) else dataset_response.get('items', [])
    jobs: list[dict] = []
    for index, record in enumerate(records, start=1):
        if not isinstance(record, dict):
            continue
        author = record.get('author') or {}
        jobs.append(
            {
                'id': f'apify-{index}',
                'title': record.get('title') or 'SAP Opportunity',
                'company': (author.get('info') if isinstance(author, dict) else '') or 'Unknown',
                'location': record.get('location') or 'Unknown',
                'url': record.get('linkedinUrl') or record.get('url') or '',
                'posted_at': record.get('postedAt') or '',
                'content': record.get('content') or record.get('text') or '',
                'source': 'apify',
            }
        )
    return jobs[:200]


def _save_jobs(paths: LocalDataPaths, ks_id: str, keywords: list[str], jobs: list[dict]) -> str:
    file = paths.jobs / f'{ks_id}.json'
    payload = {
        'keyword': ', '.join(keywords[:5]) if keywords else 'SAP Consultant',
        'keyword_set_id': ks_id,
        'jobs': jobs,
        'job_count': len(jobs),
        'updated_at': datetime.now(timezone.utc).isoformat(),
    }
    file.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding='utf-8')
    return str(file)


def onboard_user(email: str, resume_content: str) -> dict:
    paths = get_local_data_paths()
    if not resume_content.strip():
        raise ValueError('Resume content is required')

    keywords = extract_keywords(resume_content)
    if not keywords:
        raise ValueError('Could not extract meaningful keywords')

    ks_id = keyword_set_id(keywords)
    _save_keywords(paths, email, keywords, ks_id)
    resume_path = _save_resume(paths, email, resume_content)

    job_file = paths.jobs / f'{ks_id}.json'
    scrape_queued = False
    if job_file.exists():
        payload = _load_job_payload(job_file)
        jobs = payload.get('jobs', []) if isinstance(payload.get('jobs'), list) else []
        _log(paths, 'info', f'Reusing existing scrape | email={email} | keyword_set={ks_id}')
    else:
        _log(paths, 'info', f'Scraping start | email={email} | keyword_set={ks_id}')
        scrape_queued = True
        try:
            jobs = _scrape_jobs_from_apify(keywords)
        except Exception as exc:  # noqa: BLE001
            _log(paths, 'error', f'Apify scrape failed | keyword_set={ks_id} | error={exc}')
            jobs = _local_fallback_jobs(keywords)
        _save_jobs(paths, ks_id, keywords, jobs)
        _log(paths, 'info', f'Scraping end | email={email} | keyword_set={ks_id} | jobs={len(jobs)}')

    users = _load_users(paths)
    existing_user = _find_user(users, email)
    by_email = {str(user.get('email')): _enrich_user(user) for user in users if isinstance(user, dict) and user.get('email')}
    by_email[email] = {
        'email': email,
        'keywords': keywords,
        'keyword_set_id': ks_id,
        'resume_path': resume_path,
        'job_file': str(job_file),
        'job_count': len(jobs),
        'subscription_status': existing_user.get('subscription_status', 'FREE') if existing_user else 'FREE',
        'payment_id': existing_user.get('payment_id', '') if existing_user else '',
        'plan': existing_user.get('plan', DEFAULT_PLAN) if existing_user else DEFAULT_PLAN,
        'plan_amount': existing_user.get('plan_amount', DEFAULT_PLAN_PRICE_INR) if existing_user else DEFAULT_PLAN_PRICE_INR,
        'updated_at': datetime.now(timezone.utc).isoformat(),
    }
    _save_users(paths, sorted(by_email.values(), key=lambda item: item['email']))
    is_paid = by_email[email]['subscription_status'] == 'PAID'
    jobs_unlocked = len(jobs) if is_paid else min(len(jobs), FREE_JOB_LIMIT)
    return {
        'keywords': keywords,
        'keyword_set_id': ks_id,
        'scrape_queued': scrape_queued,
        'subscription_status': by_email[email]['subscription_status'],
        'jobs_unlocked': jobs_unlocked,
        'upgrade_message': '' if is_paid else f'Upgrade to unlock all jobs. Free plan shows first {FREE_JOB_LIMIT} jobs.',
    }


def get_user_jobs(email: str) -> tuple[list[dict], dict]:
    paths = get_local_data_paths()
    users = _load_users(paths)
    user = _find_user(users, email)
    if user is None:
        raise FileNotFoundError('User not found')

    ks_id = str(user.get('keyword_set_id') or '').strip()
    if not ks_id:
        raise FileNotFoundError('User keyword set not found')

    job_file = paths.jobs / f'{ks_id}.json'
    if not job_file.exists():
        raise FileNotFoundError('Job file not found')

    payload = _load_job_payload(job_file)
    jobs = payload.get('jobs', [])
    if not isinstance(jobs, list):
        jobs = []
    is_paid = str(user.get('subscription_status', 'FREE')).upper() == 'PAID'
    visible_jobs = jobs if is_paid else jobs[:FREE_JOB_LIMIT]
    meta = {
        'subscription_status': 'PAID' if is_paid else 'FREE',
        'plan': user.get('plan', DEFAULT_PLAN),
        'total_jobs': len(jobs),
        'jobs_unlocked': len(visible_jobs),
        'upgrade_required': not is_paid and len(jobs) > FREE_JOB_LIMIT,
        'upgrade_message': '' if is_paid else f'Upgrade to unlock all jobs. Free plan shows first {FREE_JOB_LIMIT} jobs.',
    }
    return visible_jobs, meta


def get_dashboard(email: str) -> dict:
    paths = get_local_data_paths()
    users = _load_users(paths)
    user = _find_user(users, email)
    if user is None:
        raise FileNotFoundError('User not found')

    jobs, meta = get_user_jobs(email)
    return {
        'email': email,
        'keyword_set_id': user.get('keyword_set_id'),
        'keywords': user.get('keywords', []),
        'job_count': meta['jobs_unlocked'],
        'total_jobs': meta['total_jobs'],
        'jobs_unlocked': meta['jobs_unlocked'],
        'subscription_status': meta['subscription_status'],
        'plan': meta['plan'],
        'upgrade_required': meta['upgrade_required'],
        'upgrade_message': meta['upgrade_message'],
        'jobs_preview': jobs[:5],
    }


def get_admin_stats() -> dict:
    paths = get_local_data_paths()
    users = _load_users(paths)
    keyword_sets = {str(user.get('keyword_set_id')) for user in users if isinstance(user, dict) and user.get('keyword_set_id')}
    total_jobs = 0
    for file in paths.jobs.glob('*.json'):
        try:
            payload = _load_job_payload(file)
            jobs = payload.get('jobs', [])
            if isinstance(jobs, list):
                total_jobs += len(jobs)
        except (OSError, json.JSONDecodeError):
            continue
    paid_users = [user for user in users if _enrich_user(user).get('subscription_status') == 'PAID']
    revenue = sum(int(_enrich_user(user).get('plan_amount', DEFAULT_PLAN_PRICE_INR)) for user in paid_users)
    return {
        'total_users': len(users),
        'total_keyword_sets': len(keyword_sets),
        'total_jobs': total_jobs,
        'total_paid_users': len(paid_users),
        'revenue': revenue,
    }


def create_payment_order(email: str, amount_inr: int | None = None) -> dict:
    key_id = os.getenv('RAZORPAY_KEY_ID', '').strip()
    key_secret = os.getenv('RAZORPAY_KEY_SECRET', '').strip()
    if not key_id or not key_secret:
        raise ValueError('Razorpay credentials are not configured')

    amount = int(amount_inr or os.getenv('BASIC_PLAN_PRICE_INR', DEFAULT_PLAN_PRICE_INR))
    if amount <= 0:
        raise ValueError('Amount must be positive')

    notes = {'email': email, 'plan': DEFAULT_PLAN}
    payload = urllib.parse.urlencode(
        {
            'amount': str(amount * 100),
            'currency': 'INR',
            'receipt': f'{_safe_email(email)}-{int(time.time())}',
            'notes[email]': notes['email'],
            'notes[plan]': notes['plan'],
        }
    ).encode('utf-8')
    req = urllib.request.Request('https://api.razorpay.com/v1/orders', data=payload, method='POST')
    req.add_header('Content-Type', 'application/x-www-form-urlencoded')
    auth = f'{key_id}:{key_secret}'.encode('utf-8')
    req.add_header('Authorization', 'Basic ' + base64.b64encode(auth).decode('utf-8'))
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            body = json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode('utf-8', errors='ignore')
        raise ValueError(f'Razorpay order creation failed: {detail[:300]}') from exc
    except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError) as exc:
        raise ValueError(f'Razorpay order creation failed: {exc}') from exc

    return {
        'order_id': body.get('id'),
        'amount': amount,
        'currency': body.get('currency', 'INR'),
        'key_id': key_id,
        'plan': DEFAULT_PLAN,
    }


def verify_payment_and_activate(
    email: str,
    razorpay_order_id: str,
    razorpay_payment_id: str,
    razorpay_signature: str,
) -> dict:
    key_secret = os.getenv('RAZORPAY_KEY_SECRET', '').strip()
    if not key_secret:
        raise ValueError('Razorpay credentials are not configured')

    payload = f'{razorpay_order_id}|{razorpay_payment_id}'
    expected_signature = hmac.new(
        key_secret.encode('utf-8'),
        payload.encode('utf-8'),
        hashlib.sha256,
    ).hexdigest()
    if not hmac.compare_digest(expected_signature, razorpay_signature):
        raise ValueError('Invalid payment signature')

    paths = get_local_data_paths()
    users = _load_users(paths)
    by_email = {str(user.get('email')): _enrich_user(user) for user in users if isinstance(user, dict) and user.get('email')}
    existing = by_email.get(email)
    if not existing:
        raise FileNotFoundError('User not found')

    updated = dict(existing)
    updated['subscription_status'] = 'PAID'
    updated['payment_id'] = razorpay_payment_id
    updated['plan'] = DEFAULT_PLAN
    updated['plan_amount'] = int(os.getenv('BASIC_PLAN_PRICE_INR', DEFAULT_PLAN_PRICE_INR))
    updated['updated_at'] = datetime.now(timezone.utc).isoformat()
    by_email[email] = updated
    _save_users(paths, sorted(by_email.values(), key=lambda item: item['email']))
    return {
        'email': email,
        'subscription_status': 'PAID',
        'payment_id': razorpay_payment_id,
        'plan': updated['plan'],
    }
