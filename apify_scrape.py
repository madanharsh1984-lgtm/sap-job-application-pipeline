"""
STEP 1 — Apify LinkedIn Post Scraper (Auto-Rotating Accounts)
=============================================================
Uses harvestapi/linkedin-post-search on Apify (same actor that sent 85 emails).

TOKEN MANAGEMENT:
  - Reads token from apify_accounts.json (managed by apify_account_creator.py)
  - If no active token found, auto-runs account creator to get a fresh $5 account
  - If monthly limit hit: flags account as exhausted, picks next account, or creates new one

APIFY ACTOR: harvestapi~linkedin-post-search
  - Searches LinkedIn posts (not jobs) — finds recruiters posting about openings
  - Extracts emails from post text → send cold outreach emails
  - maxPosts=50 per keyword, postedLimit=24h
"""

import urllib.request
import urllib.error
import json
import re
import os
import sys
import time
from datetime import datetime

sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

from config import BASE_DIR, APIFY_TOKEN as _CFG_TOKEN, JOB_TITLES

# ── PATHS ─────────────────────────────────────────────────────────────────────
OUTPUT_DIR    = BASE_DIR
OUTPUT_FILE   = os.path.join(OUTPUT_DIR, "linkedin_posts_today.json")
ACCOUNTS_FILE = os.path.join(OUTPUT_DIR, "apify_accounts.json")
LOG_FILE      = os.path.join(OUTPUT_DIR, "email_sent_log.json")

# Seed accounts file with config token if present and file doesn't exist yet
if _CFG_TOKEN and not os.path.exists(ACCOUNTS_FILE):
    import json as _json
    with open(ACCOUNTS_FILE, "w") as _f:
        _json.dump([{"email": "from-config", "password": "", "token": _CFG_TOKEN,
                     "status": "active", "credits": "managed"}], _f, indent=2)

# ── SEARCH CONFIG ─────────────────────────────────────────────────────────────
SEARCH_KEYWORDS = [t + " hiring" for t in JOB_TITLES]
MAX_POSTS_PER_KEYWORD = 50
POSTED_LIMIT          = "24h"   # only posts from last 24 hours

# ── EMAIL FILTER ──────────────────────────────────────────────────────────────
EMAIL_RE      = re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}")
SKIP_DOMAINS  = {
    "example.com", "domain.com", "email.com", "naukri.com",
    "linkedin.com", "indeed.com", "google.com", "glassdoor.com",
    "sentry.io", "github.com", "microsoft.com", "apple.com",
}

# ── APIFY API ─────────────────────────────────────────────────────────────────
APIFY_BASE    = "https://api.apify.com/v2"
ACTOR_ID      = "harvestapi~linkedin-post-search"


# ═══════════════════════════════════════════════════════════════════════════════
# TOKEN MANAGEMENT
# ═══════════════════════════════════════════════════════════════════════════════

def load_accounts() -> list:
    if not os.path.exists(ACCOUNTS_FILE):
        return []
    with open(ACCOUNTS_FILE, "r") as f:
        return json.load(f)


def save_accounts(accounts: list):
    with open(ACCOUNTS_FILE, "w") as f:
        json.dump(accounts, f, indent=2)


def get_active_token() -> str:
    """Return the most recent active Apify token, or '' if none."""
    accounts = load_accounts()
    active   = [a for a in accounts if a.get("status") == "active" and a.get("token")]
    if not active:
        return ""
    return active[-1]["token"]


def mark_token_exhausted(token: str):
    """Mark a token as exhausted so next run uses a different account."""
    accounts = load_accounts()
    for a in accounts:
        if a.get("token") == token:
            a["status"] = "exhausted"
            a["exhausted_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    save_accounts(accounts)
    print(f"  [Token] Marked exhausted: {token[:25]}...")


def ensure_active_token() -> str:
    """
    Get active token. If none exists or all are exhausted,
    automatically run the account creator to get a fresh $5 account.
    """
    token = get_active_token()
    if token:
        print(f"  [Token] Using token: {token[:25]}...")
        return token

    print("\n  [Token] No active Apify token found.")
    print("  [Token] Running account creator to get a fresh $5 account...")
    print()

    # Import and run the account creator
    try:
        import importlib.util
        creator_path = os.path.join(OUTPUT_DIR, "apify_account_creator.py")
        spec = importlib.util.spec_from_file_location("creator", creator_path)
        creator = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(creator)
        creator.main()
    except Exception as e:
        print(f"  [Token] Account creator error: {e}")
        print("  [Token] Please run apify_account_creator.py manually first.")
        sys.exit(1)

    # Try again after creator ran
    token = get_active_token()
    if not token:
        print("  [Token] Still no token after account creation. Exiting.")
        sys.exit(1)

    return token


# ═══════════════════════════════════════════════════════════════════════════════
# APIFY API CALLS
# ═══════════════════════════════════════════════════════════════════════════════

def apify_request(url: str, token: str, method: str = "GET",
                  body: dict = None) -> dict:
    """Make an authenticated request to the Apify API."""
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Content-Type",  "application/json")

    data = None
    if body:
        data = json.dumps(body).encode("utf-8")

    req.method = method
    with urllib.request.urlopen(req, data=data, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def check_credits(token: str) -> float:
    """Check remaining USD credits on the account. Returns credit amount."""
    try:
        url  = f"{APIFY_BASE}/users/me?token={token}"
        data = apify_request(url, token)
        plan = data.get("data", {}).get("plan", {})
        credits = plan.get("monthlyUsageCreditsUsd", 0)
        used    = plan.get("currentMonthlyUsageCreditsUsd", 0)
        remaining = credits - used
        print(f"  [Credits] Monthly: ${credits:.2f} | Used: ${used:.4f} | Remaining: ${remaining:.4f}")
        return remaining
    except Exception as e:
        print(f"  [Credits] Could not check credits: {e}")
        return 999.0  # assume ok


def run_actor(token: str, keyword: str) -> str:
    """
    Start a single Apify actor run for one keyword.
    Returns the dataset ID, or "" on failure.
    """
    url  = f"{APIFY_BASE}/acts/{ACTOR_ID}/runs?token={token}"
    body = {
        "searchQuery":  keyword,
        "maxPosts":     MAX_POSTS_PER_KEYWORD,
        "postedLimit":  POSTED_LIMIT,
        "sortBy":       "date",
        "proxy": {
            "useApifyProxy": True,
            "apifyProxyGroups": ["RESIDENTIAL"]
        }
    }

    try:
        resp = apify_request(url, token, method="POST", body=body)
        run_id = resp.get("data", {}).get("id", "")
        if not run_id:
            print(f"    [Actor] No run ID returned. Response: {str(resp)[:200]}")
            return ""
        print(f"    [Actor] Run started. ID: {run_id}")
        return run_id
    except urllib.error.HTTPError as e:
        body_text = e.read().decode("utf-8", errors="ignore")
        print(f"    [Actor] HTTP {e.code}: {body_text[:300]}")
        if e.code == 402 or "limit" in body_text.lower() or "credit" in body_text.lower():
            return "LIMIT_EXCEEDED"
        return ""
    except Exception as e:
        print(f"    [Actor] Error: {e}")
        return ""


def wait_for_run(token: str, run_id: str, max_wait: int = 300) -> str:
    """
    Poll the run until SUCCEEDED or FAILED.
    Returns dataset ID on success, "" on failure/timeout.
    """
    url      = f"{APIFY_BASE}/actor-runs/{run_id}?token={token}"
    deadline = time.time() + max_wait
    dots     = 0

    while time.time() < deadline:
        time.sleep(10)
        try:
            resp   = apify_request(url, token)
            status = resp.get("data", {}).get("status", "")
            dots  += 1
            print(f"    [Run] Status: {status} {'.' * dots}", end="\r")

            if status == "SUCCEEDED":
                dataset_id = resp.get("data", {}).get("defaultDatasetId", "")
                print(f"\n    [Run] SUCCEEDED. Dataset: {dataset_id}")
                return dataset_id
            elif status in ("FAILED", "ABORTED", "TIMED-OUT"):
                print(f"\n    [Run] {status}.")
                return ""
        except Exception as e:
            print(f"\n    [Run] Poll error: {e}")

    print(f"\n    [Run] Timed out after {max_wait}s.")
    return ""


def fetch_dataset(token: str, dataset_id: str) -> list:
    """Fetch all items from a dataset."""
    url  = f"{APIFY_BASE}/datasets/{dataset_id}/items?token={token}&clean=true&limit=1000"
    try:
        items = apify_request(url, token)
        if isinstance(items, list):
            return items
        # Sometimes wrapped in {"data": [...]}
        if isinstance(items, dict):
            return items.get("data", items.get("items", []))
        return []
    except Exception as e:
        print(f"    [Dataset] Fetch error: {e}")
        return []


# ═══════════════════════════════════════════════════════════════════════════════
# POST PROCESSING
# ═══════════════════════════════════════════════════════════════════════════════

def extract_emails(text: str) -> list:
    """Extract valid recruiter emails from post text."""
    if not text:
        return []
    emails = EMAIL_RE.findall(text)
    valid  = []
    for e in emails:
        domain = e.split("@")[-1].lower()
        if domain not in SKIP_DOMAINS and len(e) < 80:
            valid.append(e.lower())
    return list(dict.fromkeys(valid))  # dedupe, preserve order


def process_post(item: dict, keyword: str) -> dict:
    """Normalize an Apify harvestapi post item to our pipeline format."""
    # harvestapi returns: text, url, postedAt, author (name, url, headline, company)
    author   = item.get("author", {}) or {}
    text     = str(item.get("text", "") or item.get("content", "") or "")
    post_url = str(item.get("url", "") or item.get("postUrl", ""))

    recruiter_name = (author.get("name") or author.get("firstName", "") + " " +
                      author.get("lastName", "")).strip()
    company        = (author.get("company") or author.get("headline") or "").strip()
    posted_at      = str(item.get("postedAt") or item.get("publishedAt") or "")

    emails = extract_emails(text)
    email  = emails[0] if emails else ""

    return {
        "recruiter_name": recruiter_name,
        "company":        company,
        "email":          email,
        "has_email":      bool(email),
        "full_post_text": text,
        "post_url":       post_url,
        "posted_at":      posted_at,
        "job_title":      keyword,
        "location":       str(item.get("location", "")),
        "source":         "linkedin_post_apify",
        "search_keyword": keyword,
        "author_url":     str(author.get("url") or author.get("profileUrl", "")),
    }


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN PIPELINE
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    print("=" * 60)
    print("  STEP 1 — Apify LinkedIn Post Scraper")
    print(f"  Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)

    # ── Get token (auto-creates account if needed) ────────────────────
    token = ensure_active_token()

    # ── Check credits ─────────────────────────────────────────────────
    remaining = check_credits(token)
    if remaining <= 0.01:
        print("\n  [!] Credits exhausted on this account.")
        mark_token_exhausted(token)
        token = ensure_active_token()  # get fresh account
        remaining = check_credits(token)

    # ── Run actor for each keyword ────────────────────────────────────
    all_posts   = []
    seen_urls   = set()
    total_runs  = 0

    for keyword in SEARCH_KEYWORDS:
        print(f"\n  Keyword: {keyword}")

        run_id = run_actor(token, keyword)

        if run_id == "LIMIT_EXCEEDED":
            print("  [!] Monthly limit hit. Rotating to new account...")
            mark_token_exhausted(token)
            token  = ensure_active_token()
            run_id = run_actor(token, keyword)

        if not run_id or run_id == "LIMIT_EXCEEDED":
            print(f"    Skipping '{keyword}' — actor start failed.")
            continue

        total_runs += 1
        dataset_id = wait_for_run(token, run_id, max_wait=300)
        if not dataset_id:
            print(f"    No dataset for '{keyword}'.")
            continue

        items = fetch_dataset(token, dataset_id)
        print(f"    Fetched {len(items)} posts.")

        for item in items:
            post = process_post(item, keyword)
            url  = post["post_url"]
            if url and url not in seen_urls:
                seen_urls.add(url)
                all_posts.append(post)

    # ── Deduplicate ───────────────────────────────────────────────────
    unique_posts = []
    seen         = set()
    for p in all_posts:
        k = p["post_url"] or p["recruiter_name"] + p["posted_at"]
        if k not in seen:
            seen.add(k)
            unique_posts.append(p)

    with_email = [p for p in unique_posts if p["has_email"]]

    # ── Save output ───────────────────────────────────────────────────
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(unique_posts, f, indent=2, ensure_ascii=False)

    # Copy to Temp for cron pipeline
    temp_file = r"C:\Users\madan\AppData\Local\Temp\linkedin_posts_today.json"
    with open(temp_file, "w", encoding="utf-8") as f:
        json.dump(unique_posts, f, indent=2, ensure_ascii=False)

    # ── Summary ───────────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print(f"  Total posts scraped : {len(unique_posts)}")
    print(f"  With email          : {len(with_email)}")
    print(f"  Saved to            : {OUTPUT_FILE}")
    print("=" * 60)

    if with_email:
        print("\n  Email leads:")
        for p in with_email:
            print(f"    {p['email']:40s} | {p['company'][:30]} | {p['recruiter_name'][:25]}")

    # Save summary JSON
    summary = {
        "date":        datetime.now().strftime("%Y-%m-%d"),
        "token_used":  token[:25] + "...",
        "total_posts": len(unique_posts),
        "with_email":  len(with_email),
        "per_keyword": {kw: len([p for p in unique_posts if p["search_keyword"] == kw])
                        for kw in SEARCH_KEYWORDS},
    }
    with open(os.path.join(OUTPUT_DIR, "apify_summary.json"), "w") as f:
        json.dump(summary, f, indent=2)

    return unique_posts


if __name__ == "__main__":
    main()
