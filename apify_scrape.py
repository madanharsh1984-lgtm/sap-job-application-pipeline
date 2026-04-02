"""
STEP 1b — Apify LinkedIn Recruiter Post Scraper
================================================
Uses Apify's harvestapi/linkedin-post-search actor to find LinkedIn posts
where recruiters actively mention SAP job openings — many include direct
email addresses in the post text.

This is the BEST email discovery method — previously returned 85+ recruiter
emails with direct contact details in a single run.

APIFY ACTOR: harvestapi/linkedin-post-search
  - Searches LinkedIn by keyword
  - Returns post text, author info, likes, date
  - Recruiters often post "hiring SAP PM, email me at xyz@company.com"

COST: ~$0.02–0.05 per run on Nano plan ($6/month covers ~120 runs)

HOW IT FITS IN THE PIPELINE:
  brightdata_scrape.py  → 79 job listings  (company + title + URL)
  apify_scrape.py       → recruiter posts  (email + contact details) ← THIS FILE
  find_company_emails.py→ fills gaps for companies still missing emails
  send_sap_emails.py    → sends cold outreach to all email leads
"""

import json, re, os, sys, time, urllib.request, urllib.error
from datetime import datetime

sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)
sys.stderr.reconfigure(encoding="utf-8", line_buffering=True)

from config import APIFY_TOKEN, BASE_DIR, JOB_TITLES

# ── PATHS ──────────────────────────────────────────────────────────────────────
OUTPUT_DIR   = BASE_DIR
JOBS_FILE    = os.path.join(OUTPUT_DIR, "linkedin_posts_today.json")
APIFY_OUT    = os.path.join(OUTPUT_DIR, "apify_recruiter_posts.json")
SENT_LOG     = os.path.join(OUTPUT_DIR, "email_sent_log.json")
SUMMARY_FILE = os.path.join(OUTPUT_DIR, "apify_summary.json")

# ── APIFY CONFIG ───────────────────────────────────────────────────────────────
ACTOR_ID       = "harvestapi~linkedin-post-search"
APIFY_BASE     = "https://api.apify.com/v2"
MAX_POSTS      = 50       # posts per keyword (50 × 4 keywords = 200 posts)
POSTED_LIMIT   = "24h"   # only posts from last 24 hours
POLL_INTERVAL  = 10      # seconds between status polls
MAX_POLL_WAIT  = 300     # 5 min max wait

# ── EMAIL EXTRACTION ───────────────────────────────────────────────────────────
EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}")
SKIP_DOMAINS = {
    "example.com", "domain.com", "email.com", "naukri.com",
    "linkedin.com", "indeed.com", "google.com", "glassdoor.com",
    "sentry.io", "github.com", "microsoft.com", "apple.com",
    "brightdata.com", "sap.com", "w3.org", "schema.org",
    "2x.png", "jpeg", "jpg", "png",
}

# ── HIRING KEYWORDS (to filter relevant posts) ─────────────────────────────────
HIRING_KEYWORDS = [
    "hiring", "looking for", "urgent requirement", "vacancy", "opening",
    "required", "opportunity", "job opening", "immediate", "consultant",
    "project manager", "data migration", "reach out", "send your cv",
    "send resume", "email me", "contact me", "apply", "dm me",
    "direct message", "whatsapp", "share your profile",
]


# ==============================================================================
# APIFY API HELPERS
# ==============================================================================

def apify_request(method: str, path: str, body=None) -> tuple:
    """Make authenticated request to Apify API. Returns (status, json)."""
    url  = f"{APIFY_BASE}{path}"
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req  = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {APIFY_TOKEN}")
    req.add_header("Content-Type", "application/json")

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            raw = resp.read().decode("utf-8")
            return resp.status, json.loads(raw) if raw.strip() else {}
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="ignore")
        return e.code, {"error": raw[:300]}
    except Exception as ex:
        return 0, {"error": str(ex)}


def run_actor(keywords: list) -> str:
    """
    Start the Apify actor with all keywords in one run.
    Nano plan allows 1 concurrent run — batch all keywords together.
    Returns run_id or "".

    harvestapi/linkedin-post-search input schema (confirmed from Apify docs):
      searchQueries: list of strings (one per keyword)
      maxPosts: int  (applies to all queries)
      sort: "date" | "relevance"
    """
    input_body = {
        "searchQueries": keywords,
        "maxPosts":      MAX_POSTS,
        "sort":          "date",
        "scrapeReactions": False,
        "scrapeComments":  False,
    }

    status, resp = apify_request(
        "POST",
        f"/acts/{ACTOR_ID}/runs",
        body=input_body
    )

    if status in (200, 201):
        run_id = resp.get("data", {}).get("id", "")
        print(f"    Actor started — run ID: {run_id}")
        return run_id
    else:
        print(f"    [ERROR] Failed to start actor: {status} — {resp}")
        return ""


def poll_run(run_id: str) -> str:
    """
    Poll until run finishes. Returns dataset_id or "".
    Status: READY → RUNNING → SUCCEEDED / FAILED
    """
    deadline = time.time() + MAX_POLL_WAIT
    attempt  = 0

    while time.time() < deadline:
        time.sleep(POLL_INTERVAL)
        attempt += 1

        status, resp = apify_request("GET", f"/actor-runs/{run_id}")
        data   = resp.get("data", {})
        state  = data.get("status", "?")
        stats  = data.get("stats", {})

        print(f"    [Poll #{attempt}] status={state} | "
              f"items={stats.get('itemCount', 0)}")

        if state == "SUCCEEDED":
            dataset_id = data.get("defaultDatasetId", "")
            print(f"    Run complete — dataset: {dataset_id}")
            return dataset_id
        elif state in ("FAILED", "ABORTED", "TIMED-OUT"):
            print(f"    [ERROR] Run ended with status: {state}")
            return ""
        # else READY / RUNNING — keep polling

    print(f"    [TIMEOUT] Run did not complete within {MAX_POLL_WAIT}s")
    return ""


def fetch_dataset(dataset_id: str) -> list:
    """Fetch all items from the Apify dataset."""
    status, resp = apify_request(
        "GET",
        f"/datasets/{dataset_id}/items?clean=true&format=json&limit=1000"
    )
    if status == 200:
        if isinstance(resp, list):
            return resp
        return resp.get("items", [])
    print(f"    [ERROR] Fetching dataset failed: {status} — {resp}")
    return []


# ==============================================================================
# POST PROCESSING
# ==============================================================================

def extract_emails(text: str) -> list:
    if not text:
        return []
    emails = EMAIL_RE.findall(str(text))
    valid  = []
    for e in emails:
        domain = e.split("@")[-1].lower()
        if (domain not in SKIP_DOMAINS
                and len(e) < 80
                and "." in domain
                and not domain.endswith(".png")
                and not domain.endswith(".jpg")):
            valid.append(e.lower())
    return list(dict.fromkeys(valid))


def is_hiring_post(text: str) -> bool:
    if not text:
        return False
    text_lower = text.lower()
    return any(kw in text_lower for kw in HIRING_KEYWORDS)


def process_post(record: dict) -> dict | None:
    """Convert raw Apify record to our pipeline format.
    
    harvestapi/linkedin-post-search field names (confirmed 2026-04-02):
      record["content"]              — post text (string)
      record["author"]["name"]       — recruiter name
      record["author"]["linkedinUrl"]— profile URL
      record["author"]["info"]       — headline/title
      record["linkedinUrl"]          — post URL
      record["postedAt"]             — date posted
    """
    # Post text — field is "content" in this actor's schema
    text = str(
        record.get("content") or
        record.get("text") or
        record.get("postText") or ""
    )

    # Also extract email hints from contentAttributes (mailto: links)
    content_attrs = record.get("contentAttributes") or []
    extra_emails = []
    if isinstance(content_attrs, list):
        for attr in content_attrs:
            tl = attr.get("textLink", "") or ""
            if tl.startswith("mailto:"):
                extra_emails.append(tl[7:].strip().lower())
            elif "@" in tl and not tl.startswith("http"):
                extra_emails.append(tl.strip().lower())

    author   = record.get("author") or {}
    if isinstance(author, dict):
        name    = author.get("name") or author.get("fullName") or ""
        profile = author.get("linkedinUrl") or author.get("profileUrl") or author.get("url") or ""
        headline= author.get("info") or author.get("headline") or ""
    else:
        name, profile, headline = str(author), "", ""

    company  = ""
    if " at " in headline:
        company = headline.split(" at ")[-1].strip()[:60]
    elif " @ " in headline:
        company = headline.split(" @ ")[-1].strip()[:60]

    date_posted = str(
        record.get("postedAt") or record.get("date") or
        record.get("publishedAt") or datetime.now().strftime("%Y-%m-%d")
    )
    post_url = str(record.get("linkedinUrl") or record.get("url") or record.get("postUrl") or profile)

    # Only process hiring-relevant posts
    if not is_hiring_post(text):
        return None

    emails = extract_emails(text) + extra_emails
    # deduplicate, preserve order
    seen_e = set()
    unique_emails = []
    for e in emails:
        if e not in seen_e:
            seen_e.add(e)
            unique_emails.append(e)
    email  = unique_emails[0] if unique_emails else ""

    return {
        "recruiter_name":  name or "Hiring Manager",
        "company":         company,
        "email":           email,
        "has_email":       bool(email),
        "full_post_text":  text[:1000],
        "post_url":        post_url,
        "posted_at":       date_posted,
        "job_title":       "SAP Hiring Post",
        "location":        "India",
        "source":          "apify_linkedin_posts",
        "search_keyword":  record.get("query") or record.get("searchQuery") or "",
        "num_likes":       record.get("likesCount") or record.get("likes") or 0,
        "recruiter_linkedin": profile,
    }


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    print("=" * 62)
    print("  Apify LinkedIn Recruiter Post Scraper")
    print(f"  Date   : {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"  Token  : {APIFY_TOKEN[:12]}****")
    print(f"  Actor  : {ACTOR_ID}")
    print("=" * 62)

    if not APIFY_TOKEN:
        print("\n  ERROR: APIFY_TOKEN not set in config.py")
        return []

    # ── Quick token check ────────────────────────────────────────────────
    print("\n  Verifying Apify token...")
    status, resp = apify_request("GET", "/users/me")
    if status == 200:
        user = resp.get("data", {})
        print(f"  Logged in as: {user.get('username','?')} "
              f"(plan: {user.get('plan',{}).get('id','?')})")
    elif status == 401:
        print("  ERROR: Invalid Apify token. Check config.py")
        return []
    else:
        print(f"  [WARN] Token check returned {status} — proceeding anyway")

    # ── Load existing jobs (from Bright Data scraper) ────────────────────
    existing_jobs = []
    if os.path.exists(JOBS_FILE):
        try:
            with open(JOBS_FILE, encoding="utf-8") as f:
                existing_jobs = json.load(f)
            print(f"\n  Existing job records: {len(existing_jobs)}")
        except Exception:
            pass

    # ── Load sent log (avoid resending) ─────────────────────────────────
    sent_emails = set()
    if os.path.exists(SENT_LOG):
        try:
            with open(SENT_LOG, encoding="utf-8") as f:
                log = json.load(f)
            sent_emails = {e.get("email","").lower() for e in log if e.get("email")}
        except Exception:
            pass

    # ── Run actor — ALL keywords in one batch ────────────────────────────
    print(f"\n  Starting actor with {len(JOB_TITLES)} keywords...")
    for kw in JOB_TITLES:
        print(f"    - {kw}")

    run_id = run_actor(JOB_TITLES)
    if not run_id:
        print("  ERROR: Could not start actor.")
        return []

    # ── Poll until complete ──────────────────────────────────────────────
    print(f"\n  Polling run {run_id}...")
    dataset_id = poll_run(run_id)
    if not dataset_id:
        print("  ERROR: Run did not succeed.")
        return []

    # ── Fetch dataset ────────────────────────────────────────────────────
    print(f"\n  Fetching dataset {dataset_id}...")
    raw_records = fetch_dataset(dataset_id)
    print(f"  Raw records fetched: {len(raw_records)}")

    # ── Process posts ────────────────────────────────────────────────────
    processed  = []
    seen_posts = set()

    for rec in raw_records:
        post = process_post(rec)
        if not post:
            continue
        key = post.get("post_url") or post["full_post_text"][:80]
        if key in seen_posts:
            continue
        seen_posts.add(key)

        # Skip already-sent emails
        if post["email"] and post["email"] in sent_emails:
            continue

        processed.append(post)

    with_email = [p for p in processed if p["has_email"]]

    print(f"\n  Hiring posts found    : {len(processed)}")
    print(f"  With recruiter email  : {len(with_email)}")

    # ── Save Apify-only output ───────────────────────────────────────────
    with open(APIFY_OUT, "w", encoding="utf-8") as f:
        json.dump(processed, f, indent=2, ensure_ascii=False)

    # ── Merge with existing jobs file ────────────────────────────────────
    # Apify recruiter posts go FIRST — they have emails, highest priority
    combined = processed + existing_jobs
    # Deduplicate by email (keep first occurrence)
    seen_emails_combined = set()
    final = []
    for r in combined:
        email = (r.get("email") or "").lower()
        if email and email in seen_emails_combined:
            continue
        if email:
            seen_emails_combined.add(email)
        final.append(r)

    with open(JOBS_FILE, "w", encoding="utf-8") as f:
        json.dump(final, f, indent=2, ensure_ascii=False)

    try:
        temp = r"C:\Users\madan\AppData\Local\Temp\linkedin_posts_today.json"
        with open(temp, "w", encoding="utf-8") as f:
            json.dump(final, f, indent=2, ensure_ascii=False)
    except Exception:
        pass

    # ── Summary ──────────────────────────────────────────────────────────
    summary = {
        "date":            datetime.now().strftime("%Y-%m-%d"),
        "run_id":          run_id,
        "dataset_id":      dataset_id,
        "raw_records":     len(raw_records),
        "hiring_posts":    len(processed),
        "with_email":      len(with_email),
        "combined_total":  len(final),
    }
    with open(SUMMARY_FILE, "w") as f:
        json.dump(summary, f, indent=2)

    print()
    print("=" * 62)
    print(f"  Hiring posts found    : {len(processed)}")
    print(f"  With recruiter email  : {len(with_email)}")
    print(f"  Combined total        : {len(final)} records")
    print(f"  Saved to              : {JOBS_FILE}")
    print("=" * 62)

    if with_email:
        print("\n  Recruiter email leads:")
        for p in with_email[:20]:
            print(f"    {p['email']:40s} | {p['recruiter_name'][:30]}")
    else:
        print("\n  No emails in posts this run — find_company_emails.py will")
        print("  fill gaps from company website lookup.")

    return final


if __name__ == "__main__":
    main()
