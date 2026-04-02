"""
STEP 1b -- LinkedIn Recruiter Post Email Finder
===============================================
Finds recruiter posts on LinkedIn that contain email addresses,
using multiple FREE discovery methods:

METHOD 1: Google Custom Search API (free: 100/day, ~5-10 posts per search)
  - Searches "site:linkedin.com/posts SAP hiring email India"
  - Extracts email addresses directly from Google snippets (no LinkedIn login needed)

METHOD 2: Bing Web Search (free via direct HTTP)
  - Same queries via Bing search results
  - Parses snippets for emails

METHOD 3: DuckDuckGo HTML search (completely free, no key)
  - Final fallback with no rate limits

All methods extract emails directly from search snippets,
so we never need to actually open LinkedIn (avoids auth/blocking issues).

Output: email leads appended to linkedin_posts_today.json for send_sap_emails.py
"""

import json
import re
import os
import sys
import time
import urllib.request
import urllib.error
import urllib.parse
from datetime import datetime

sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)
sys.stderr.reconfigure(encoding="utf-8", line_buffering=True)

from config import BRIGHTDATA_API_KEY, BASE_DIR

# ── PATHS ──────────────────────────────────────────────────────────────────────
OUTPUT_DIR      = BASE_DIR
JOBS_FILE       = os.path.join(OUTPUT_DIR, "linkedin_posts_today.json")
POSTS_OUTPUT    = os.path.join(OUTPUT_DIR, "linkedin_recruiter_posts.json")
COMBINED_OUTPUT = os.path.join(OUTPUT_DIR, "linkedin_posts_today.json")
SENT_LOG        = os.path.join(OUTPUT_DIR, "email_sent_log.json")
SUMMARY_FILE    = os.path.join(OUTPUT_DIR, "brightdata_posts_summary.json")

# ── EMAIL REGEX ────────────────────────────────────────────────────────────────
EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}")
SKIP_DOMAINS = {
    "example.com", "domain.com", "email.com", "naukri.com",
    "linkedin.com", "indeed.com", "google.com", "glassdoor.com",
    "sentry.io", "github.com", "microsoft.com", "apple.com",
    "brightdata.com", "sap.com", "w3.org", "schema.org",
    "wixpress.com", "cloudflare.com",
}

# ── SEARCH QUERIES ─────────────────────────────────────────────────────────────
SEARCH_QUERIES = [
    'site:linkedin.com "SAP" "hiring" "email" India',
    'site:linkedin.com "SAP S4HANA" "consultant" "send CV" India',
    'site:linkedin.com "SAP Project Manager" "vacancy" "contact" India',
    'site:linkedin.com "SAP Data Migration" "urgent" "reach out" India',
    'site:linkedin.com "SAP PM" "hiring" "@gmail.com" OR "@" India 2024 OR 2025',
    'linkedin.com "SAP" "hiring" "email your resume" India',
    'linkedin.com "SAP" "urgently required" "email" India site:linkedin.com',
]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}


# ==============================================================================
# HELPERS
# ==============================================================================

def extract_emails(text: str) -> list:
    if not text:
        return []
    emails = EMAIL_RE.findall(str(text))
    valid = []
    for e in emails:
        domain = e.split("@")[-1].lower()
        if (domain not in SKIP_DOMAINS
                and len(e) < 80
                and "." in domain
                and not domain.endswith(".png")
                and not domain.endswith(".jpg")):
            valid.append(e.lower())
    return list(dict.fromkeys(valid))


def load_sent_emails() -> set:
    if not os.path.exists(SENT_LOG):
        return set()
    try:
        with open(SENT_LOG, encoding="utf-8") as f:
            log = json.load(f)
        return {entry.get("email", "").lower() for entry in log if entry.get("email")}
    except Exception:
        return set()


def http_get(url: str, timeout: int = 20) -> str:
    """Simple HTTP GET with a browser-like user agent. Returns HTML or ''."""
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            charset = resp.headers.get_content_charset() or "utf-8"
            return resp.read().decode(charset, errors="ignore")
    except Exception as ex:
        print(f"    [HTTP] {ex}")
        return ""


# ==============================================================================
# METHOD 1: DuckDuckGo HTML search (completely free, no API key)
# ==============================================================================

def duckduckgo_search(query: str) -> list:
    """
    Search DuckDuckGo HTML results and extract emails from snippets.
    Returns list of lead dicts.
    """
    encoded = urllib.parse.quote_plus(query)
    url = f"https://html.duckduckgo.com/html/?q={encoded}"

    html = http_get(url, timeout=30)
    if not html:
        return []

    leads = []

    # Extract result snippets from DDG HTML
    snippet_re = re.compile(
        r'<a[^>]+class="result__snippet"[^>]*>(.*?)</a>',
        re.DOTALL | re.IGNORECASE
    )
    # Also check result URLs and titles
    url_re = re.compile(
        r'<a[^>]+class="result__url"[^>]*>(.*?)</a>',
        re.DOTALL | re.IGNORECASE
    )

    snippets = snippet_re.findall(html)
    urls_found = url_re.findall(html)

    # Strip HTML tags
    tag_re = re.compile(r"<[^>]+>")

    for i, snippet in enumerate(snippets):
        clean = tag_re.sub(" ", snippet).strip()
        emails = extract_emails(clean)
        if not emails:
            # Also check full page for obfuscated emails like "name [at] company [dot] com"
            obf = re.findall(
                r'([a-zA-Z0-9._%+\-]+)\s*[\[\(]at[\]\)]\s*([a-zA-Z0-9.\-]+)\s*[\[\(]dot[\]\)]\s*([a-zA-Z]{2,})',
                clean, re.IGNORECASE
            )
            if obf:
                emails = [f"{u}@{d}.{t}".lower() for u, d, t in obf]

        if emails:
            # Get source URL
            src_url = ""
            if i < len(urls_found):
                src_url = tag_re.sub("", urls_found[i]).strip()

            for email in emails:
                leads.append({
                    "recruiter_name":  "",
                    "company":         "",
                    "email":           email,
                    "has_email":       True,
                    "full_post_text":  clean[:500],
                    "post_url":        src_url,
                    "posted_at":       datetime.now().strftime("%Y-%m-%d"),
                    "job_title":       "SAP Hiring Post",
                    "location":        "India",
                    "source":          "duckduckgo_search",
                    "search_keyword":  query[:60],
                })

    return leads


# ==============================================================================
# METHOD 2: Bing search (free, no API key via HTML)
# ==============================================================================

def bing_search(query: str) -> list:
    """
    Search Bing HTML results and extract emails from snippets.
    Returns list of lead dicts.
    """
    encoded = urllib.parse.quote_plus(query)
    url = f"https://www.bing.com/search?q={encoded}&count=20"

    html = http_get(url, timeout=30)
    if not html:
        return []

    leads = []

    # Bing result blocks
    result_re = re.compile(
        r'<li class="b_algo".*?</li>',
        re.DOTALL | re.IGNORECASE
    )
    tag_re = re.compile(r"<[^>]+>")

    for block in result_re.findall(html):
        clean = tag_re.sub(" ", block).strip()
        emails = extract_emails(clean)

        if emails:
            # Extract URL from block
            url_match = re.search(r'href="(https?://[^"]+)"', block)
            src_url = url_match.group(1) if url_match else ""

            for email in emails:
                leads.append({
                    "recruiter_name":  "",
                    "company":         "",
                    "email":           email,
                    "has_email":       True,
                    "full_post_text":  clean[:500],
                    "post_url":        src_url,
                    "posted_at":       datetime.now().strftime("%Y-%m-%d"),
                    "job_title":       "SAP Hiring Post",
                    "location":        "India",
                    "source":          "bing_search",
                    "search_keyword":  query[:60],
                })

    return leads


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    print("=" * 62)
    print("  STEP 1b -- LinkedIn Recruiter Post Email Finder")
    print(f"  Date  : {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 62)

    # Load existing job results from Bright Data Jobs scraper
    existing_jobs = []
    if os.path.exists(JOBS_FILE):
        try:
            with open(JOBS_FILE, encoding="utf-8") as f:
                existing_jobs = json.load(f)
            print(f"  Loaded {len(existing_jobs)} records from brightdata_scrape.py")
        except Exception as e:
            print(f"  [WARN] Could not load jobs file: {e}")
    else:
        print("  [WARN] No linkedin_posts_today.json found — starting fresh")

    already_sent = load_sent_emails()
    all_leads    = []

    # ── DuckDuckGo search (primary free method) ──────────────────────────
    print(f"\n  Searching DuckDuckGo for SAP hiring posts with emails...")
    ddg_leads = []
    for i, query in enumerate(SEARCH_QUERIES):
        print(f"  [{i+1}/{len(SEARCH_QUERIES)}] {query[:65]}...")
        leads = duckduckgo_search(query)
        print(f"    Found {len(leads)} email leads")
        ddg_leads.extend(leads)
        time.sleep(2)  # polite delay

    print(f"\n  DuckDuckGo total: {len(ddg_leads)} leads")
    all_leads.extend(ddg_leads)

    # ── Bing search (secondary free method) ─────────────────────────────
    if len(all_leads) < 5:
        print(f"\n  DuckDuckGo found few leads. Trying Bing...")
        bing_leads = []
        for i, query in enumerate(SEARCH_QUERIES[:4]):
            print(f"  [{i+1}/4] {query[:65]}...")
            leads = bing_search(query)
            print(f"    Found {len(leads)} email leads")
            bing_leads.extend(leads)
            time.sleep(2)
        print(f"  Bing total: {len(bing_leads)} leads")
        all_leads.extend(bing_leads)

    # ── Deduplicate ──────────────────────────────────────────────────────
    seen_emails = set()
    seen_posts  = set()
    final_leads = []

    for lead in all_leads:
        email = lead.get("email", "").lower()

        # Skip already-sent emails
        if email and email in already_sent:
            continue

        # Deduplicate by email
        if email:
            if email in seen_emails:
                continue
            seen_emails.add(email)
        else:
            # No email — keep if unique post
            key = lead.get("post_url") or lead["full_post_text"][:80]
            if key in seen_posts:
                continue
            seen_posts.add(key)

        final_leads.append(lead)

    with_email = [l for l in final_leads if l["has_email"]]

    # ── Save outputs ─────────────────────────────────────────────────────
    try:
        with open(POSTS_OUTPUT, "w", encoding="utf-8") as f:
            json.dump(final_leads, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"  [WARN] Could not save posts output: {e}")

    combined = existing_jobs + final_leads
    try:
        with open(COMBINED_OUTPUT, "w", encoding="utf-8") as f:
            json.dump(combined, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"  [WARN] Could not save combined output: {e}")

    try:
        temp_file = r"C:\Users\madan\AppData\Local\Temp\linkedin_posts_today.json"
        with open(temp_file, "w", encoding="utf-8") as f:
            json.dump(combined, f, indent=2, ensure_ascii=False)
    except Exception:
        pass

    # ── Summary ──────────────────────────────────────────────────────────
    summary = {
        "date":           datetime.now().strftime("%Y-%m-%d"),
        "raw_leads":      len(all_leads),
        "unique_leads":   len(final_leads),
        "with_email":     len(with_email),
        "combined_total": len(combined),
    }
    try:
        with open(SUMMARY_FILE, "w") as f:
            json.dump(summary, f, indent=2)
    except Exception:
        pass

    print()
    print("=" * 62)
    print(f"  Raw leads found     : {len(all_leads)}")
    print(f"  Unique leads        : {len(final_leads)}")
    print(f"  With email          : {len(with_email)}")
    print(f"  Combined output     : {len(combined)} total records")
    print(f"  Saved to            : {COMBINED_OUTPUT}")
    print("=" * 62)

    if with_email:
        print("\n  Email leads found:")
        for p in with_email[:20]:
            name = p.get("recruiter_name") or p.get("source", "")
            print(f"    {p['email']:40s} | {name[:30]}")
    else:
        print("\n  No emails found in search snippets this run.")
        print("  This is normal when LinkedIn posts don't show email text in snippets.")
        print("  The jobs scraper (brightdata_scrape.py) is the primary email source.")

    return combined


if __name__ == "__main__":
    main()
