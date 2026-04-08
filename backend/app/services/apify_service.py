"""
Apify integration service — shared job scraping.

Key principle: Apify is triggered ONLY once per unique keyword_hash.
Results are stored centrally and shared across all users with the same hash.
"""

import json
import logging
import time

import httpx

from backend.app.core.config import settings

logger = logging.getLogger(__name__)

# ── Email extraction helpers (ported from legacy apify_scrape.py) ─────────
import re

EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}")
SKIP_DOMAINS = frozenset({
    "example.com", "domain.com", "email.com", "naukri.com",
    "linkedin.com", "indeed.com", "google.com", "glassdoor.com",
    "sentry.io", "github.com", "microsoft.com", "apple.com",
    "brightdata.com", "sap.com", "w3.org", "schema.org",
})

HIRING_KEYWORDS = [
    "hiring", "looking for", "urgent requirement", "vacancy", "opening",
    "required", "opportunity", "job opening", "immediate", "consultant",
    "project manager", "data migration", "reach out", "send your cv",
    "send resume", "email me", "contact me", "apply", "dm me",
]


def _extract_emails(text: str) -> list[str]:
    """Extract valid recruiter emails from text."""
    if not text:
        return []
    emails = EMAIL_RE.findall(str(text))
    valid = []
    for e in emails:
        domain = e.split("@")[-1].lower()
        if (domain not in SKIP_DOMAINS and len(e) < 80
                and "." in domain
                and not domain.endswith((".png", ".jpg"))):
            valid.append(e.lower())
    return list(dict.fromkeys(valid))


def _is_hiring_post(text: str) -> bool:
    """Check if text contains hiring-related keywords."""
    if not text:
        return False
    text_lower = text.lower()
    return any(kw in text_lower for kw in HIRING_KEYWORDS)


def run_apify_scrape(keywords: list[str]) -> list[dict]:
    """
    Trigger Apify actor, poll until complete, fetch and process results.

    This is a SYNCHRONOUS function designed to run inside a Celery worker.
    Returns a list of processed job dicts ready for DB insertion.

    Args:
        keywords: Normalized keyword list to search for.

    Returns:
        List of job dicts with keys: title, company, location, email,
        post_url, job_data, source, external_id.
    """
    if not settings.APIFY_TOKEN:
        logger.error("APIFY_TOKEN not configured")
        return []

    headers = {
        "Authorization": f"Bearer {settings.APIFY_TOKEN}",
        "Content-Type": "application/json",
    }

    # ── Step 1: Start actor run ──────────────────────────────────────────
    input_body = {
        "searchQueries": keywords,
        "maxPosts": settings.APIFY_MAX_POSTS,
        "sort": "date",
        "scrapeReactions": False,
        "scrapeComments": False,
    }

    with httpx.Client(timeout=60) as client:
        resp = client.post(
            f"{settings.APIFY_BASE_URL}/acts/{settings.APIFY_ACTOR_ID}/runs",
            headers=headers,
            json=input_body,
        )

    if resp.status_code not in (200, 201):
        logger.error("Failed to start Apify actor: %s — %s", resp.status_code, resp.text[:300])
        return []

    run_id = resp.json().get("data", {}).get("id", "")
    if not run_id:
        logger.error("No run_id in Apify response")
        return []

    logger.info("Apify actor started — run_id=%s", run_id)

    # ── Step 2: Poll until complete ──────────────────────────────────────
    deadline = time.time() + settings.APIFY_MAX_POLL_WAIT
    dataset_id = ""

    while time.time() < deadline:
        time.sleep(settings.APIFY_POLL_INTERVAL)
        with httpx.Client(timeout=60) as client:
            poll_resp = client.get(
                f"{settings.APIFY_BASE_URL}/actor-runs/{run_id}",
                headers=headers,
            )
        if poll_resp.status_code != 200:
            continue

        data = poll_resp.json().get("data", {})
        state = data.get("status", "?")
        logger.info("Poll: status=%s", state)

        if state == "SUCCEEDED":
            dataset_id = data.get("defaultDatasetId", "")
            break
        elif state in ("FAILED", "ABORTED", "TIMED-OUT"):
            logger.error("Apify run ended with status: %s", state)
            return []

    if not dataset_id:
        logger.error("Apify run timed out after %ds", settings.APIFY_MAX_POLL_WAIT)
        return []

    # ── Step 3: Fetch dataset ────────────────────────────────────────────
    with httpx.Client(timeout=60) as client:
        ds_resp = client.get(
            f"{settings.APIFY_BASE_URL}/datasets/{dataset_id}/items",
            headers=headers,
            params={"clean": "true", "format": "json", "limit": "1000"},
        )

    if ds_resp.status_code != 200:
        logger.error("Failed to fetch dataset: %s", ds_resp.status_code)
        return []

    raw_records = ds_resp.json()
    if not isinstance(raw_records, list):
        raw_records = raw_records.get("items", [])

    logger.info("Fetched %d raw records from Apify", len(raw_records))

    # ── Step 4: Process records ──────────────────────────────────────────
    processed = []
    seen_keys = set()

    for record in raw_records:
        text = str(
            record.get("content") or record.get("text") or record.get("postText") or ""
        )

        if not _is_hiring_post(text):
            continue

        author = record.get("author") or {}
        if isinstance(author, dict):
            name = author.get("name") or author.get("fullName") or ""
            headline = author.get("info") or author.get("headline") or ""
        else:
            name, headline = str(author), ""

        company = ""
        if " at " in headline:
            company = headline.split(" at ")[-1].strip()[:60]
        elif " @ " in headline:
            company = headline.split(" @ ")[-1].strip()[:60]

        post_url = str(
            record.get("linkedinUrl") or record.get("url") or record.get("postUrl") or ""
        )

        # Dedup by post URL or text prefix
        dedup_key = post_url or text[:80]
        if dedup_key in seen_keys:
            continue
        seen_keys.add(dedup_key)

        emails = _extract_emails(text)
        email = emails[0] if emails else None

        job_dict = {
            "title": f"SAP Hiring Post — {name or 'Recruiter'}" if not company else f"{company} — SAP Hiring",
            "company": company or None,
            "location": "India",
            "email": email,
            "post_url": post_url or None,
            "source": "apify_linkedin_posts",
            "external_id": post_url or None,
            "job_data": json.dumps({
                "recruiter_name": name or "Hiring Manager",
                "company": company,
                "email": email or "",
                "has_email": bool(email),
                "full_post_text": text[:1000],
                "post_url": post_url,
                "posted_at": str(record.get("postedAt") or record.get("date") or ""),
                "search_keyword": record.get("query") or record.get("searchQuery") or "",
                "num_likes": record.get("likesCount") or record.get("likes") or 0,
            }, ensure_ascii=False),
        }
        processed.append(job_dict)

    logger.info("Processed %d hiring posts", len(processed))
    return processed
