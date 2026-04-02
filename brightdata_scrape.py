"""
STEP 1 — Bright Data LinkedIn Jobs Scraper
==========================================
Uses Bright Data's Dataset API (datasets/v3/trigger) to scrape LinkedIn
job listings by keyword. Much more reliable and scalable than Apify or
JobSpy — no monthly limits to rotate around.

BRIGHT DATA API DETAILS:
  Endpoint  : POST https://api.brightdata.com/datasets/v3/trigger
  Dataset ID: gd_lpfll7v5hcqtkxl6l  (LinkedIn Job Listings — discover by keyword)
  Auth      : Bearer {BRIGHTDATA_API_KEY}
  Polling   : GET /datasets/v3/snapshot/{snapshot_id} → 200=ready, 202=pending

FLOW:
  1. Trigger a scrape job for each SAP keyword → get snapshot_id
  2. Poll until all snapshots are ready (200 OK)
  3. Fetch JSON data from each snapshot
  4. Extract emails from job descriptions
  5. Save to linkedin_posts_today.json (same format used by send_sap_emails.py)

PRICING (trial account):
  ~$0.001 per record. 50 jobs × 4 keywords = 200 records ≈ $0.20/day
"""

import json
import re
import os
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime

sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

from config import BRIGHTDATA_API_KEY, BASE_DIR, JOB_TITLES

# ── PATHS ──────────────────────────────────────────────────────────────────────
OUTPUT_DIR  = BASE_DIR
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "linkedin_posts_today.json")
SUMMARY_FILE = os.path.join(OUTPUT_DIR, "brightdata_summary.json")

# ── BRIGHT DATA CONFIG ─────────────────────────────────────────────────────────
BD_API_BASE  = "https://api.brightdata.com/datasets/v3"
DATASET_ID   = "gd_lpfll7v5hcqtkxl6l"   # LinkedIn Job Listings — discover by keyword
JOBS_PER_KW  = 50                          # max jobs per keyword
POLL_INTERVAL = 15                         # seconds between status polls
MAX_POLL_WAIT = 600                        # 10 min max wait per snapshot

# ── EMAIL EXTRACTION ───────────────────────────────────────────────────────────
EMAIL_RE    = re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}")
SKIP_DOMAINS = {
    "example.com", "domain.com", "email.com", "naukri.com",
    "linkedin.com", "indeed.com", "google.com", "glassdoor.com",
    "sentry.io", "github.com", "microsoft.com", "apple.com",
    "brightdata.com", "sap.com",
}


# ═══════════════════════════════════════════════════════════════════════════════
# API HELPERS
# ═══════════════════════════════════════════════════════════════════════════════

def bd_request(method: str, path: str, body=None, params: dict = None) -> tuple:
    """
    Make an authenticated request to Bright Data API.
    Returns (status_code, parsed_json_or_list).
    """
    url = f"{BD_API_BASE}{path}"
    if params:
        qs = "&".join(f"{k}={v}" for k, v in params.items())
        url = f"{url}?{qs}"

    data = json.dumps(body).encode("utf-8") if body is not None else None

    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {BRIGHTDATA_API_KEY}")
    req.add_header("Content-Type", "application/json")

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            raw = resp.read().decode("utf-8")
            return resp.status, json.loads(raw) if raw.strip() else {}
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="ignore")
        return e.code, {"error": raw}
    except Exception as ex:
        return 0, {"error": str(ex)}


def trigger_scrape(keyword: str) -> str:
    """
    Trigger a LinkedIn job search for one keyword.
    Returns snapshot_id, or "" on failure.

    Valid field values (from Bright Data docs):
      time_range      : "Past 24 hours" | "Past week" | "Past month"
      remote          : "Remote" | "Hybrid" | "On-site"
      experience_level: "Internship" | "Entry level" | "Associate" |
                        "Mid-Senior level" | "Director" | "Executive"
      job_type        : "Full-time" | "Part-time" | "Contract" | "Temporary"
    """
    params = {
        "dataset_id":      DATASET_ID,
        "include_errors":  "true",
        "type":            "discover_new",
        "discover_by":     "keyword",
        "limit_per_input": str(JOBS_PER_KW),
    }
    # Body must be {"input": [...]} for the trigger endpoint
    body = {"input": [{
        "keyword":          keyword,
        "location":         "India",
        "country":          "IN",
        "time_range":       "Past week",
        "remote":           "Remote",
        "experience_level": "Mid-Senior level",
        "job_type":         "Full-time",
        "company":          "",
        "location_radius":  "",
    }]}

    status, resp = bd_request("POST", "/trigger", body=body, params=params)

    if status == 200:
        snap_id = resp.get("snapshot_id", "")
        print(f"    [Trigger] snapshot_id: {snap_id}")
        return snap_id
    else:
        print(f"    [Trigger] Failed {status}: {str(resp)[:200]}")
        return ""


def poll_snapshot(snapshot_id: str) -> list:
    """
    Poll until snapshot is ready. Returns list of job records or [].
    200 = data ready
    202 = still processing, wait and retry
    """
    deadline = time.time() + MAX_POLL_WAIT
    attempt  = 0

    while time.time() < deadline:
        time.sleep(POLL_INTERVAL)
        attempt += 1

        status, resp = bd_request(
            "GET", f"/snapshot/{snapshot_id}",
            params={"format": "json"}
        )

        print(f"    [Poll #{attempt}] status={status}", end="")

        if status == 200:
            # resp is either a list of records or a dict with 'data' key
            if isinstance(resp, list):
                print(f" -- {len(resp)} records ready")
                return resp
            elif isinstance(resp, dict):
                data = resp.get("data", resp.get("items", []))
                if isinstance(data, list):
                    print(f" -- {len(data)} records ready")
                    return data
            print(f" -- ready but unexpected format: {str(resp)[:100]}")
            return []

        elif status == 202:
            pct = resp.get("progress", {}).get("percent", "?") if isinstance(resp, dict) else "?"
            print(f" -- still processing ({pct}%)...")
            continue

        else:
            print(f" -- Error: {str(resp)[:150]}")
            return []

    print(f"\n    [Poll] Timed out after {MAX_POLL_WAIT}s")
    return []


# ═══════════════════════════════════════════════════════════════════════════════
# POST PROCESSING
# ═══════════════════════════════════════════════════════════════════════════════

def extract_emails(text: str) -> list:
    """Extract valid recruiter emails from text."""
    if not text:
        return []
    emails = EMAIL_RE.findall(str(text))
    valid  = []
    for e in emails:
        domain = e.split("@")[-1].lower()
        if domain not in SKIP_DOMAINS and len(e) < 80:
            valid.append(e.lower())
    return list(dict.fromkeys(valid))


def process_job(item: dict, keyword: str) -> dict:
    """
    Normalize a Bright Data LinkedIn job record to our pipeline format.

    Bright Data job record fields (from gd_lpfll7v5hcqtkxl6l):
      job_posting_id, url, job_title, company_name, company_url,
      location, workplace_type, job_description, apply_link,
      posted_time, salary, experience_level, job_type
    """
    desc    = str(item.get("job_description") or "")
    title   = str(item.get("job_title") or "")
    company = str(item.get("company_name") or "")
    url     = str(item.get("url") or item.get("apply_link") or "")
    loc     = str(item.get("location") or "")
    posted  = str(item.get("posted_time") or item.get("posted_date") or "")

    # Extract recruiter email from description
    emails = extract_emails(desc)
    email  = emails[0] if emails else ""

    # Try to get a contact name from description
    # Common patterns: "Contact: John Doe" / "reach out to Jane Smith"
    recruiter_name = company  # fallback to company name
    name_match = re.search(
        r"(?:contact|reach out to|send.*?to|email)\s+([A-Z][a-z]+ [A-Z][a-z]+)",
        desc, re.IGNORECASE
    )
    if name_match:
        recruiter_name = name_match.group(1)

    return {
        "recruiter_name":  recruiter_name,
        "company":         company,
        "email":           email,
        "has_email":       bool(email),
        "job_title":       title,
        "location":        loc,
        "post_url":        url,
        "posted_at":       posted,
        "full_post_text":  desc,
        "workplace_type":  str(item.get("workplace_type") or ""),
        "salary":          str(item.get("salary") or ""),
        "experience":      str(item.get("experience_level") or ""),
        "search_keyword":  keyword,
        "source":          "linkedin_brightdata",
        "job_posting_id":  str(item.get("job_posting_id") or ""),
    }


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    print("=" * 62)
    print("  STEP 1 — Bright Data LinkedIn Jobs Scraper")
    print(f"  Date  : {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"  API   : {BRIGHTDATA_API_KEY[:8]}****")
    print("=" * 62)

    # ── Quick API connectivity check ──────────────────────────────────
    print("\n  Checking API connectivity...")
    # Use a known valid endpoint: list snapshots (even empty list = auth OK)
    status, resp = bd_request("GET", "/snapshots", params={"dataset_id": DATASET_ID, "limit": "1"})
    if status in (200, 206, 404):
        print(f"  API key OK (status {status})\n")
    elif status == 401:
        print(f"  [ERROR] Invalid API key (401 Unauthorized).")
        print("  Check BRIGHTDATA_API_KEY in config.py")
        sys.exit(1)
    else:
        # Non-fatal — proceed anyway, trigger will catch real errors
        print(f"  [WARN] Health check returned {status}, proceeding anyway...\n")

    # ── Trigger all keyword searches ──────────────────────────────────
    snapshots = {}   # keyword → snapshot_id

    for keyword in JOB_TITLES:
        search_kw = f"SAP {keyword}" if not keyword.upper().startswith("SAP") else keyword
        print(f"  Triggering: {search_kw}")
        snap_id = trigger_scrape(search_kw)
        if snap_id:
            snapshots[keyword] = snap_id
        time.sleep(2)   # small gap between triggers

    if not snapshots:
        print("\n  [ERROR] No snapshots triggered. Check API key and dataset access.")
        sys.exit(1)

    print(f"\n  {len(snapshots)}/{len(JOB_TITLES)} searches triggered. Polling for results...\n")

    # ── Poll all snapshots and collect results ────────────────────────
    all_posts  = []
    seen_ids   = set()
    per_kw     = {}

    for keyword, snap_id in snapshots.items():
        print(f"  Polling: {keyword} (snapshot: {snap_id})")
        records = poll_snapshot(snap_id)

        kw_posts = []
        for item in records:
            post = process_job(item, keyword)
            uid  = post["job_posting_id"] or post["post_url"] or (post["company"] + post["job_title"])
            if uid and uid not in seen_ids:
                seen_ids.add(uid)
                kw_posts.append(post)
                all_posts.append(post)

        per_kw[keyword] = len(kw_posts)
        with_email      = len([p for p in kw_posts if p["has_email"]])
        print(f"    -- {len(kw_posts)} jobs, {with_email} with email\n")

    # ── Save results ──────────────────────────────────────────────────
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_posts, f, indent=2, ensure_ascii=False)

    # Also copy to Temp for cron pipeline
    temp_file = r"C:\Users\madan\AppData\Local\Temp\linkedin_posts_today.json"
    try:
        with open(temp_file, "w", encoding="utf-8") as f:
            json.dump(all_posts, f, indent=2, ensure_ascii=False)
    except Exception:
        pass

    # ── Stats ─────────────────────────────────────────────────────────
    with_email = [p for p in all_posts if p["has_email"]]
    est_cost   = len(all_posts) * 0.001

    summary = {
        "date":         datetime.now().strftime("%Y-%m-%d"),
        "total_jobs":   len(all_posts),
        "with_email":   len(with_email),
        "est_cost_usd": round(est_cost, 4),
        "per_keyword":  per_kw,
    }
    with open(SUMMARY_FILE, "w") as f:
        json.dump(summary, f, indent=2)

    print("=" * 62)
    print(f"  Total jobs scraped : {len(all_posts)}")
    print(f"  With email         : {len(with_email)}")
    print(f"  Estimated cost     : ~${est_cost:.4f}")
    print(f"  Saved to           : {OUTPUT_FILE}")
    print("=" * 62)

    if with_email:
        print("\n  Email leads found:")
        for p in with_email:
            print(f"    {p['email']:40s} | {p['company'][:28]} | {p['job_title'][:30]}")

    return all_posts


if __name__ == "__main__":
    main()
