from __future__ import annotations

import hashlib
import json
import re
import time
import urllib.error
import urllib.request

from sqlalchemy.orm import Session

from app.models.job import Job
from app.models.keyword_set import KeywordSet
from app.models.user_keyword_map import UserKeywordMap
from app.core.settings import settings

MAX_JOBS_TO_INGEST = 200
APIFY_BASE_URL = 'https://api.apify.com/v2'
MIN_KEYWORD_LENGTH = 4
MAX_KEYWORDS = 30


def extract_keywords(content: str) -> list[str]:
    tokens = re.findall(r"[A-Za-z0-9+#./-]+", content or '')
    candidates = [token for token in tokens if len(token) > MIN_KEYWORD_LENGTH]
    return normalize_keywords(candidates)[:MAX_KEYWORDS]


def normalize_keywords(keywords: list[str]) -> list[str]:
    normalized = {keyword.strip().lower() for keyword in keywords if keyword and keyword.strip()}
    return sorted(normalized)


def keyword_hash(normalized_keywords: list[str]) -> str:
    joined = '|'.join(normalized_keywords)
    return hashlib.sha256(joined.encode('utf-8')).hexdigest()


def upsert_user_keyword_set(db: Session, user_id: int, normalized_keywords: list[str]) -> tuple[KeywordSet, bool]:
    if not normalized_keywords:
        raise ValueError('No keywords available')

    hashed_keywords = keyword_hash(normalized_keywords)
    keyword_set = db.query(KeywordSet).filter(KeywordSet.keyword_hash == hashed_keywords).first()
    created = False
    if keyword_set is None:
        keyword_set = KeywordSet(
            keyword_hash=hashed_keywords,
            normalized_keywords=json.dumps(normalized_keywords),
        )
        db.add(keyword_set)
        db.flush()
        created = True

    existing_map = (
        db.query(UserKeywordMap)
        .filter(
            UserKeywordMap.user_id == user_id,
            UserKeywordMap.keyword_set_id == keyword_set.id,
        )
        .first()
    )
    if existing_map is None:
        db.add(UserKeywordMap(user_id=user_id, keyword_set_id=keyword_set.id))

    db.commit()
    db.refresh(keyword_set)
    return keyword_set, created


def list_jobs_for_user(db: Session, user_id: int) -> list[Job]:
    return (
        db.query(Job)
        .join(UserKeywordMap, UserKeywordMap.keyword_set_id == Job.keyword_set_id)
        .filter(UserKeywordMap.user_id == user_id)
        .order_by(Job.id.desc())
        .limit(MAX_JOBS_TO_INGEST)
        .all()
    )


def _apify_request(method: str, path: str, body: dict | None = None) -> tuple[int, dict | list]:
    url = f'{APIFY_BASE_URL}{path}'
    data = json.dumps(body).encode('utf-8') if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header('Authorization', f'Bearer {settings.APIFY_TOKEN}')
    req.add_header('Content-Type', 'application/json')

    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            payload = response.read().decode('utf-8')
            return response.status, json.loads(payload) if payload.strip() else {}
    except urllib.error.HTTPError as exc:
        payload = exc.read().decode('utf-8', errors='ignore')
        return exc.code, {'error': payload[:1000]}
    except Exception as exc:
        return 0, {'error': str(exc)}


def _parse_apify_record(record: dict) -> dict:
    author = record.get('author') or {}
    author_name = author.get('name') if isinstance(author, dict) else ''
    return {
        'title': record.get('title') or record.get('headline') or 'SAP Opportunity',
        'company': (author.get('info') if isinstance(author, dict) else '') or '',
        'location': record.get('location') or '',
        'url': record.get('linkedinUrl') or record.get('url') or '',
        'posted_at': record.get('postedAt') or record.get('date') or '',
        'search_keyword': record.get('query') or record.get('searchQuery') or '',
        'author_name': author_name or '',
        'content': record.get('content') or record.get('text') or '',
        'source': 'apify_linkedin_posts',
        'raw': record,
    }


def scrape_jobs_from_apify(normalized_keywords: list[str]) -> list[dict]:
    if not settings.APIFY_TOKEN:
        raise RuntimeError('APIFY_TOKEN is not configured')

    status, run_response = _apify_request(
        'POST',
        f"/acts/{settings.APIFY_ACTOR_ID}/runs",
        body={
            'searchQueries': normalized_keywords,
            'maxPosts': settings.APIFY_MAX_POSTS,
            'sort': 'date',
            'scrapeReactions': False,
            'scrapeComments': False,
        },
    )
    if status not in (200, 201):
        raise RuntimeError(f'Failed to start Apify actor: status={status} response={run_response}')

    run_id = (run_response or {}).get('data', {}).get('id')
    if not run_id:
        raise RuntimeError('Apify actor run id missing')

    dataset_id = ''
    for _ in range(30):
        time.sleep(2)
        run_status_code, run_status_response = _apify_request('GET', f'/actor-runs/{run_id}')
        if run_status_code != 200:
            continue
        run_data = (run_status_response or {}).get('data', {})
        status_value = run_data.get('status')
        if status_value == 'SUCCEEDED':
            dataset_id = run_data.get('defaultDatasetId', '')
            break
        if status_value in ('FAILED', 'ABORTED', 'TIMED-OUT'):
            raise RuntimeError(f'Apify actor finished with status={status_value}')

    if not dataset_id:
        raise RuntimeError('Apify actor did not provide dataset id')

    dataset_status, dataset_response = _apify_request(
        'GET',
        f'/datasets/{dataset_id}/items?clean=true&format=json&limit=1000',
    )
    if dataset_status != 200:
        raise RuntimeError(f'Failed to fetch Apify dataset: status={dataset_status}')

    records = dataset_response if isinstance(dataset_response, list) else dataset_response.get('items', [])
    parsed = [_parse_apify_record(record) for record in records if isinstance(record, dict)]
    return parsed[:MAX_JOBS_TO_INGEST]


def store_jobs_for_keyword_set(db: Session, keyword_set_id: int, jobs: list[dict]) -> int:
    db.query(Job).filter(Job.keyword_set_id == keyword_set_id).delete()
    inserted = 0
    for record in jobs:
        db.add(Job(keyword_set_id=keyword_set_id, job_data=json.dumps(record)))
        inserted += 1
    db.commit()
    return inserted
