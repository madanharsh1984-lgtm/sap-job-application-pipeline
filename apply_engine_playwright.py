"""
Playwright-based Apply Engine
=============================
Replaces Selenium-driven LinkedIn/Naukri apply automation with:
- Stealth browser setup
- Optional captcha solving (2Captcha / CapMonster)
- Session persistence (local file or Redis)
- Retry + failover (proxy/session refresh)
- Parallel processing workers
- Structured run metrics
"""

from __future__ import annotations

import json
import os
import re
import time
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

import requests
try:
    from playwright.sync_api import BrowserContext, Error as PlaywrightError, Page, sync_playwright
except Exception:  # noqa: BLE001
    BrowserContext = Any  # type: ignore
    Page = Any  # type: ignore
    PlaywrightError = Exception  # type: ignore
    sync_playwright = None  # type: ignore

try:
    from playwright_stealth import stealth_sync
except Exception:  # noqa: BLE001
    stealth_sync = None


BASE_DIR = Path(os.getenv('BASE_DIR', Path(__file__).resolve().parent))
LOG_DIR = Path(os.getenv('LOG_DIR', str(BASE_DIR)))
SESSIONS_DIR = Path(os.getenv('PLAYWRIGHT_SESSION_DIR', str(BASE_DIR / '.playwright_sessions')))
SESSIONS_DIR.mkdir(parents=True, exist_ok=True)


@dataclass
class ApplyTarget:
    platform: str
    title: str
    location: str


@dataclass
class ApplyResult:
    platform: str
    title: str
    location: str
    status: str
    reason: str = ''
    applied_count: int = 0
    captcha_triggered: bool = False
    started_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    finished_at: str = ''


@dataclass
class EngineConfig:
    linkedin_email: str
    linkedin_pass: str
    naukri_email: str
    naukri_pass: str
    resume_path: str
    headless: bool = True
    workers: int = 5
    max_retries: int = 2
    user_agent: str = (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/124.0.0.0 Safari/537.36'
    )
    use_api_apply: bool = True
    redis_url: str = ''
    captcha_provider: str = ''
    captcha_api_key: str = ''
    proxy_list: list[str] = field(default_factory=list)


class CaptchaSolver:
    def solve(self, site_key: str, page_url: str) -> str:
        raise NotImplementedError


class TwoCaptchaSolver(CaptchaSolver):
    def __init__(self, api_key: str):
        self.api_key = api_key

    def solve(self, site_key: str, page_url: str) -> str:
        in_resp = requests.post(
            'http://2captcha.com/in.php',
            data={
                'key': self.api_key,
                'method': 'userrecaptcha',
                'googlekey': site_key,
                'pageurl': page_url,
                'json': 1,
            },
            timeout=30,
        ).json()
        if in_resp.get('status') != 1:
            raise RuntimeError(f"2Captcha submit failed: {in_resp}")

        request_id = in_resp.get('request')
        for _ in range(24):
            time.sleep(5)
            out_resp = requests.get(
                'http://2captcha.com/res.php',
                params={'key': self.api_key, 'action': 'get', 'id': request_id, 'json': 1},
                timeout=30,
            ).json()
            if out_resp.get('status') == 1:
                return str(out_resp.get('request'))
            if out_resp.get('request') != 'CAPCHA_NOT_READY':
                raise RuntimeError(f"2Captcha solve failed: {out_resp}")
        raise RuntimeError('2Captcha timed out')


class CapMonsterSolver(CaptchaSolver):
    def __init__(self, api_key: str):
        self.api_key = api_key

    def solve(self, site_key: str, page_url: str) -> str:
        create = requests.post(
            'https://api.capmonster.cloud/createTask',
            json={
                'clientKey': self.api_key,
                'task': {
                    'type': 'RecaptchaV2TaskProxyless',
                    'websiteURL': page_url,
                    'websiteKey': site_key,
                },
            },
            timeout=30,
        ).json()
        task_id = create.get('taskId')
        if not task_id:
            raise RuntimeError(f'CapMonster task create failed: {create}')

        for _ in range(24):
            time.sleep(5)
            result = requests.post(
                'https://api.capmonster.cloud/getTaskResult',
                json={'clientKey': self.api_key, 'taskId': task_id},
                timeout=30,
            ).json()
            if result.get('status') == 'ready':
                return str((result.get('solution') or {}).get('gRecaptchaResponse', ''))
            if result.get('status') == 'failed':
                raise RuntimeError(f'CapMonster solve failed: {result}')
        raise RuntimeError('CapMonster timed out')


class SessionStore:
    def __init__(self, redis_url: str):
        self.redis_url = redis_url.strip()
        self.redis_client = None
        if self.redis_url:
            try:
                import redis  # type: ignore

                self.redis_client = redis.from_url(self.redis_url, decode_responses=True)
            except Exception:  # noqa: BLE001
                self.redis_client = None

    def _key(self, platform: str, username: str) -> str:
        safe = re.sub(r'[^a-zA-Z0-9_-]+', '_', username)
        return f'playwright_session:{platform}:{safe}'

    def load(self, platform: str, username: str) -> list[dict]:
        key = self._key(platform, username)
        if self.redis_client:
            raw = self.redis_client.get(key)
            return json.loads(raw) if raw else []
        file = SESSIONS_DIR / f'{key}.json'
        if file.exists():
            return json.loads(file.read_text(encoding='utf-8'))
        return []

    def save(self, platform: str, username: str, cookies: list[dict]) -> None:
        key = self._key(platform, username)
        payload = json.dumps(cookies, ensure_ascii=False)
        if self.redis_client:
            self.redis_client.set(key, payload)
            return
        file = SESSIONS_DIR / f'{key}.json'
        file.write_text(payload, encoding='utf-8')


class PlaywrightApplyEngine:
    def __init__(self, config: EngineConfig):
        self.config = config
        self.session_store = SessionStore(config.redis_url)
        self.captcha_solver = self._build_solver(config.captcha_provider, config.captcha_api_key)
        self.metrics: list[ApplyResult] = []

    @staticmethod
    def _build_solver(provider: str, api_key: str) -> CaptchaSolver | None:
        provider = (provider or '').strip().lower()
        if not provider or not api_key:
            return None
        if provider == '2captcha':
            return TwoCaptchaSolver(api_key)
        if provider == 'capmonster':
            return CapMonsterSolver(api_key)
        return None

    def _new_context(self, playwright, proxy: str | None = None):
        launch_args: dict[str, Any] = {'headless': self.config.headless}
        if proxy:
            launch_args['proxy'] = {'server': proxy}
        browser = playwright.chromium.launch(**launch_args)
        context = browser.new_context(
            user_agent=self.config.user_agent,
            locale='en-US',
            timezone_id='Asia/Kolkata',
            viewport={'width': 1366, 'height': 768},
            ignore_https_errors=True,
        )
        context.add_init_script(
            """
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
            window.chrome = window.chrome || { runtime: {} };
            Object.defineProperty(navigator, 'plugins', { get: () => [1,2,3] });
            Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
            """
        )
        return browser, context

    def _prepare_page(self, context: BrowserContext) -> Page:
        page = context.new_page()
        if stealth_sync:
            stealth_sync(page)
        return page

    @staticmethod
    def _site_key_from_page(page: Page) -> str:
        for selector in ['[data-sitekey]', '.g-recaptcha', 'iframe[src*="recaptcha"]']:
            try:
                el = page.query_selector(selector)
                if not el:
                    continue
                key = el.get_attribute('data-sitekey')
                if key:
                    return key
            except Exception:  # noqa: BLE001
                continue
        return ''

    def _solve_captcha_if_needed(self, page: Page) -> bool:
        text = (page.content() or '').lower()
        if 'captcha' not in text and 'recaptcha' not in text:
            return False
        if not self.captcha_solver:
            return True
        site_key = self._site_key_from_page(page)
        if not site_key:
            return True
        token = self.captcha_solver.solve(site_key, page.url)
        page.evaluate(
            """
            (token) => {
              const area = document.querySelector('textarea[name="g-recaptcha-response"]');
              if (area) {
                area.value = token;
                area.dispatchEvent(new Event('change', { bubbles: true }));
              }
            }
            """,
            token,
        )
        return True

    def _apply_saved_session(self, context: BrowserContext, platform: str, username: str) -> None:
        cookies = self.session_store.load(platform, username)
        if cookies:
            context.add_cookies(cookies)

    def _persist_session(self, context: BrowserContext, platform: str, username: str) -> None:
        self.session_store.save(platform, username, context.cookies())

    def _login_linkedin(self, page: Page) -> None:
        page.goto('https://www.linkedin.com/login', wait_until='domcontentloaded')
        page.fill('#username', self.config.linkedin_email)
        page.fill('#password', self.config.linkedin_pass)
        page.click("button[type='submit']")
        page.wait_for_timeout(3000)

    def _login_naukri(self, page: Page) -> None:
        page.goto('https://www.naukri.com/nlogin/login', wait_until='domcontentloaded')
        page.fill("input[type='text'], input[placeholder*='Email']", self.config.naukri_email)
        page.fill("input[type='password']", self.config.naukri_pass)
        page.click("button[type='submit'], button.loginButton")
        page.wait_for_timeout(3000)

    def _capture_linkedin_apply_api(self, page: Page) -> list[dict]:
        captured: list[dict] = []

        def handle_request(req):
            url = req.url or ''
            host = (urlparse(url).hostname or '').lower()
            is_linkedin = host in {'linkedin.com', 'www.linkedin.com'}
            if is_linkedin and ('jobs-apply' in url or '/easyApply' in url):
                captured.append({'url': url, 'method': req.method, 'headers': req.headers})

        page.on('request', handle_request)
        return captured

    @staticmethod
    def _build_linkedin_search_url(title: str) -> str:
        q = requests.utils.quote(title)
        return f'https://www.linkedin.com/jobs/search/?keywords={q}&f_LF=f_AL&f_WT=2&f_TPR=r86400'

    def _run_linkedin_ui_apply(self, page: Page, target: ApplyTarget) -> int:
        page.goto(self._build_linkedin_search_url(target.title), wait_until='domcontentloaded')
        page.wait_for_timeout(3000)
        buttons = page.query_selector_all("button:has-text('Easy Apply')")
        applied = 0
        for btn in buttons[:10]:
            try:
                btn.click(timeout=3000)
                page.wait_for_timeout(800)
                upload = page.query_selector("input[type='file']")
                if upload and self.config.resume_path:
                    upload.set_input_files(self.config.resume_path)
                for selector in [
                    "button:has-text('Submit application')",
                    "button:has-text('Review')",
                    "button:has-text('Next')",
                ]:
                    for _ in range(3):
                        nxt = page.query_selector(selector)
                        if nxt:
                            nxt.click(timeout=2000)
                            page.wait_for_timeout(500)
                applied += 1
            except Exception:  # noqa: BLE001
                continue
        return applied

    def _run_naukri_ui_apply(self, page: Page, target: ApplyTarget) -> int:
        title_slug = target.title.lower().replace(' ', '-')
        loc_slug = target.location.lower().replace(' ', '-')
        url = f'https://www.naukri.com/{title_slug}-jobs'
        if loc_slug and loc_slug != 'remote':
            url += f'-in-{loc_slug}'
        page.goto(url, wait_until='domcontentloaded')
        page.wait_for_timeout(3000)
        applied = 0
        buttons = page.query_selector_all("button:has-text('Apply'), button:has-text('Quick Apply')")
        for btn in buttons[:10]:
            try:
                btn.click(timeout=3000)
                page.wait_for_timeout(1000)
                submit = page.query_selector("button:has-text('Apply'), button:has-text('Submit')")
                if submit:
                    submit.click(timeout=3000)
                applied += 1
            except Exception:  # noqa: BLE001
                continue
        return applied

    def _attempt_linkedin_api_apply(self, captured_requests: list[dict]) -> int:
        if not self.config.use_api_apply:
            return 0
        # Hook point for replay logic. Keep disabled until a stable endpoint contract is known.
        return 0 if not captured_requests else 0

    def process_target(self, target: ApplyTarget) -> ApplyResult:
        result = ApplyResult(platform=target.platform, title=target.title, location=target.location, status='FAILED')
        if sync_playwright is None:
            result.reason = 'Playwright is not installed. Run: python -m pip install playwright playwright-stealth && python -m playwright install chromium'
            result.finished_at = datetime.utcnow().isoformat()
            return result
        credentials = {
            'linkedin': self.config.linkedin_email,
            'naukri': self.config.naukri_email,
        }
        username = credentials.get(target.platform, '')

        for attempt in range(self.config.max_retries + 1):
            proxy = None
            if self.config.proxy_list:
                proxy = self.config.proxy_list[min(attempt, len(self.config.proxy_list) - 1)]
            try:
                with sync_playwright() as p:
                    browser, context = self._new_context(p, proxy=proxy)
                    try:
                        self._apply_saved_session(context, target.platform, username)
                        page = self._prepare_page(context)

                        if target.platform == 'linkedin':
                            self._login_linkedin(page)
                            captured = self._capture_linkedin_apply_api(page)
                            ui_applied = self._run_linkedin_ui_apply(page, target)
                            api_applied = self._attempt_linkedin_api_apply(captured)
                            result.applied_count = ui_applied + api_applied
                        elif target.platform == 'naukri':
                            self._login_naukri(page)
                            result.applied_count = self._run_naukri_ui_apply(page, target)
                        else:
                            result.reason = f'Unsupported platform: {target.platform}'
                            return result

                        if self._solve_captcha_if_needed(page):
                            result.captcha_triggered = True

                        self._persist_session(context, target.platform, username)
                        result.status = 'SUCCESS' if result.applied_count > 0 else 'NO_MATCH'
                        result.reason = '' if result.applied_count > 0 else 'No applyable jobs discovered'
                        result.finished_at = datetime.utcnow().isoformat()
                        return result
                    finally:
                        context.close()
                        browser.close()
            except (PlaywrightError, requests.RequestException, RuntimeError) as exc:
                result.reason = f'Attempt {attempt + 1} failed: {exc}'
                time.sleep(1.5)
                continue

        result.finished_at = datetime.utcnow().isoformat()
        return result

    def run_parallel(self, targets: list[ApplyTarget]) -> dict:
        self.metrics = []
        with ThreadPoolExecutor(max_workers=max(1, min(self.config.workers, 10))) as pool:
            futures = [pool.submit(self.process_target, t) for t in targets]
            for fut in as_completed(futures):
                self.metrics.append(fut.result())

        payload = {
            'generated_at': datetime.utcnow().isoformat(),
            'total_targets': len(targets),
            'successful_targets': sum(1 for item in self.metrics if item.status == 'SUCCESS'),
            'total_applied': sum(item.applied_count for item in self.metrics),
            'captcha_triggers': sum(1 for item in self.metrics if item.captcha_triggered),
            'results': [item.__dict__ for item in self.metrics],
        }
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        (LOG_DIR / 'playwright_apply_metrics.json').write_text(
            json.dumps(payload, indent=2, ensure_ascii=False),
            encoding='utf-8',
        )
        return payload


def _config_from_runtime() -> EngineConfig:
    from config import (  # type: ignore
        JOB_TITLES,
        NAUKRI_LOCATIONS,
        LINKEDIN_EMAIL,
        LINKEDIN_PASS,
        NAUKRI_EMAIL,
        NAUKRI_PASS,
        RESUME_PATH,
        LOG_DIR as CFG_LOG_DIR,
        BASE_DIR as CFG_BASE_DIR,
    )

    global BASE_DIR, LOG_DIR, SESSIONS_DIR
    BASE_DIR = Path(str(CFG_BASE_DIR))
    LOG_DIR = Path(str(CFG_LOG_DIR))
    SESSIONS_DIR = Path(os.getenv('PLAYWRIGHT_SESSION_DIR', str(BASE_DIR / '.playwright_sessions')))
    SESSIONS_DIR.mkdir(parents=True, exist_ok=True)

    cfg = EngineConfig(
        linkedin_email=LINKEDIN_EMAIL,
        linkedin_pass=LINKEDIN_PASS,
        naukri_email=NAUKRI_EMAIL,
        naukri_pass=NAUKRI_PASS,
        resume_path=str(RESUME_PATH),
        headless=os.getenv('PLAYWRIGHT_HEADLESS', 'true').lower() == 'true',
        workers=int(os.getenv('PLAYWRIGHT_WORKERS', '5')),
        max_retries=int(os.getenv('PLAYWRIGHT_MAX_RETRIES', '2')),
        use_api_apply=os.getenv('PLAYWRIGHT_USE_API_APPLY', 'true').lower() == 'true',
        redis_url=os.getenv('PLAYWRIGHT_REDIS_URL', ''),
        captcha_provider=os.getenv('CAPTCHA_PROVIDER', ''),
        captcha_api_key=os.getenv('CAPTCHA_API_KEY', ''),
        proxy_list=[p.strip() for p in os.getenv('PLAYWRIGHT_PROXY_LIST', '').split(',') if p.strip()],
    )

    # Keep for caller convenience
    cfg._job_titles = JOB_TITLES  # type: ignore[attr-defined]
    cfg._naukri_locations = NAUKRI_LOCATIONS  # type: ignore[attr-defined]
    return cfg


def run_linkedin_apply() -> dict:
    cfg = _config_from_runtime()
    engine = PlaywrightApplyEngine(cfg)
    targets = [ApplyTarget(platform='linkedin', title=title, location='Remote') for title in cfg._job_titles]  # type: ignore[attr-defined]
    summary = engine.run_parallel(targets)
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return summary


def run_naukri_apply() -> dict:
    cfg = _config_from_runtime()
    engine = PlaywrightApplyEngine(cfg)
    targets = [
        ApplyTarget(platform='naukri', title=title, location=location)
        for title in cfg._job_titles  # type: ignore[attr-defined]
        for location in cfg._naukri_locations  # type: ignore[attr-defined]
    ]
    summary = engine.run_parallel(targets)
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return summary


if __name__ == '__main__':
    mode = os.getenv('APPLY_PLATFORM', 'linkedin').strip().lower()
    if mode == 'naukri':
        run_naukri_apply()
    else:
        run_linkedin_apply()
