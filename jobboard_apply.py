"""
jobboard_apply.py — IIMJobs + Hirist + Instahyre Auto-Apply
============================================================
Searches 4 SAP keywords on IIMJobs, Hirist, and Instahyre.
Extracts job listings, deduplicates, logs results, and
opens apply links in Chrome (or triggers quick-apply where available).

Note: These portals require login for actual applying.
This script handles:
  - IIMJobs: scrapes job listings, opens apply pages
  - Hirist: scrapes job listings via API, logs them
  - Instahyre: scrapes listings, logs them
  
Results saved to: jobboard_applied_log.json
"""

import json, os, sys, time, re
import urllib.request, urllib.parse
from datetime import datetime, timedelta

BASE_DIR = r"C:\Users\madan\OneDrive\Desktop\Linkdin Job Application"
LOG_FILE = os.path.join(BASE_DIR, "jobboard_applied_log.json")

KEYWORDS = [
    "SAP S4 HANA Project Manager",
    "SAP Project Manager",
    "SAP SD MM Consultant",
    "SAP Data Migration Consultant",
]

RESEND_DAYS = 30  # don't re-apply to same job within 30 days

# ── HELPERS ───────────────────────────────────────────────────────────────────

def load_log():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, encoding="utf-8") as f:
            return json.load(f)
    return []

def save_log(log):
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2, ensure_ascii=False)

def already_applied(job_id: str, log: list) -> bool:
    cutoff = datetime.now() - timedelta(days=RESEND_DAYS)
    for e in log:
        if e.get("job_id") == job_id:
            try:
                if datetime.fromisoformat(e["timestamp"]) > cutoff:
                    return True
            except Exception:
                return True
    return False

def fetch_url(url: str, headers: dict = None, timeout=30) -> str:
    req = urllib.request.Request(url)
    req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    if headers:
        for k, v in headers.items():
            req.add_header(k, v)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="ignore")
    except Exception as e:
        return f"ERROR: {e}"

# ── IIMJOBS SCRAPER ───────────────────────────────────────────────────────────

def scrape_iimjobs(keyword: str) -> list:
    """Scrape IIMJobs search results for keyword."""
    jobs = []
    encoded = urllib.parse.quote_plus(keyword)
    url = f"https://www.iimjobs.com/search/result?search_term={encoded}&exp=10-20&location=India"

    print(f"    IIMJobs: {url}")
    html = fetch_url(url)
    if html.startswith("ERROR"):
        print(f"    ✗ IIMJobs error: {html}")
        return []

    # Extract job cards using regex
    # Pattern: job title, company, location, job URL
    job_pattern = re.findall(
        r'href="(https://www\.iimjobs\.com/j/[^"]+)"[^>]*>([^<]{5,100})</a>',
        html
    )
    company_pattern = re.findall(r'class="[^"]*company[^"]*"[^>]*>([^<]{2,60})</[^>]+>', html)

    seen = set()
    for i, (url_match, title) in enumerate(job_pattern[:15]):
        title = title.strip()
        if not title or title in seen:
            continue
        seen.add(title)
        # Filter SAP-relevant jobs
        if not any(kw.lower() in title.lower() for kw in ["sap", "erp", "s/4", "s4"]):
            continue
        company = company_pattern[i].strip() if i < len(company_pattern) else "Unknown"
        job_id = hashlib.md5(url_match.encode()).hexdigest()[:12]
        jobs.append({
            "job_id": f"iimjobs_{job_id}",
            "title": title,
            "company": company,
            "url": url_match,
            "source": "IIMJobs",
            "keyword": keyword,
        })

    print(f"    IIMJobs: {len(jobs)} SAP jobs found")
    return jobs

# ── HIRIST SCRAPER ────────────────────────────────────────────────────────────

def scrape_hirist(keyword: str) -> list:
    """Scrape Hirist.tech search results."""
    jobs = []
    encoded = urllib.parse.quote_plus(keyword)
    url = f"https://www.hirist.tech/search/?q={encoded}&location=India&experience=10"

    print(f"    Hirist: {url}")
    html = fetch_url(url)
    if html.startswith("ERROR"):
        print(f"    ✗ Hirist error: {html}")
        return []

    # Extract job info
    titles   = re.findall(r'class="[^"]*job[_-]title[^"]*"[^>]*>([^<]{5,100})</[^>]+>', html)
    companies= re.findall(r'class="[^"]*company[_-]name[^"]*"[^>]*>([^<]{2,80})</[^>]+>', html)
    links    = re.findall(r'href="(/j/[^"]{10,100})"', html)

    seen = set()
    for i, title in enumerate(titles[:15]):
        title = title.strip()
        if not title or title in seen:
            continue
        seen.add(title)
        if not any(kw.lower() in title.lower() for kw in ["sap", "erp", "s/4", "s4"]):
            continue
        company = companies[i].strip() if i < len(companies) else "Unknown"
        link    = f"https://www.hirist.tech{links[i]}" if i < len(links) else url
        job_id  = hashlib.md5(link.encode()).hexdigest()[:12]
        jobs.append({
            "job_id": f"hirist_{job_id}",
            "title": title,
            "company": company,
            "url": link,
            "source": "Hirist",
            "keyword": keyword,
        })

    print(f"    Hirist: {len(jobs)} SAP jobs found")
    return jobs

# ── INSTAHYRE SCRAPER ─────────────────────────────────────────────────────────

def scrape_instahyre(keyword: str) -> list:
    """Scrape Instahyre search results."""
    jobs = []
    encoded = urllib.parse.quote_plus(keyword)
    url = f"https://www.instahyre.com/search-jobs/?q={encoded}&l=India"

    print(f"    Instahyre: {url}")
    html = fetch_url(url)
    if html.startswith("ERROR"):
        print(f"    ✗ Instahyre error: {html}")
        return []

    titles   = re.findall(r'"title"\s*:\s*"([^"]{5,100})"', html)
    companies= re.findall(r'"company"\s*:\s*"([^"]{2,80})"', html)
    job_ids  = re.findall(r'"id"\s*:\s*(\d{4,12})', html)

    seen = set()
    for i, title in enumerate(titles[:15]):
        title = title.strip()
        if not title or title in seen:
            continue
        seen.add(title)
        if not any(kw.lower() in title.lower() for kw in ["sap", "erp", "s/4", "s4"]):
            continue
        company = companies[i].strip() if i < len(companies) else "Unknown"
        jid = job_ids[i] if i < len(job_ids) else str(i)
        link = f"https://www.instahyre.com/job/{jid}/"
        jobs.append({
            "job_id": f"instahyre_{jid}",
            "title": title,
            "company": company,
            "url": link,
            "source": "Instahyre",
            "keyword": keyword,
        })

    print(f"    Instahyre: {len(jobs)} SAP jobs found")
    return jobs

# ── INDEED INDIA SCRAPER ──────────────────────────────────────────────────────

def scrape_indeed(keyword: str) -> list:
    """Scrape Indeed India search results."""
    jobs = []
    encoded = urllib.parse.quote_plus(keyword)
    url = f"https://in.indeed.com/jobs?q={encoded}&l=India&sc=0kf%3Aattr(DSQF7)%3B&fromage=3"

    print(f"    Indeed: {url}")
    html = fetch_url(url)
    if html.startswith("ERROR"):
        print(f"    ✗ Indeed error: {html}")
        return []

    # Extract job info from Indeed
    title_pattern   = re.findall(r'"jobTitle"\s*:\s*"([^"]{5,100})"', html)
    company_pattern = re.findall(r'"company"\s*:\s*"([^"]{2,80})"', html)
    jk_pattern      = re.findall(r'"jk"\s*:\s*"([a-f0-9]{16})"', html)

    seen = set()
    for i, title in enumerate(title_pattern[:15]):
        title = title.strip()
        if not title or title in seen:
            continue
        seen.add(title)
        if not any(kw.lower() in title.lower() for kw in ["sap", "erp", "s/4", "s4"]):
            continue
        company = company_pattern[i].strip() if i < len(company_pattern) else "Unknown"
        jk = jk_pattern[i] if i < len(jk_pattern) else ""
        link = f"https://in.indeed.com/viewjob?jk={jk}" if jk else url
        jobs.append({
            "job_id": f"indeed_{jk or i}",
            "title": title,
            "company": company,
            "url": link,
            "source": "Indeed India",
            "keyword": keyword,
        })

    print(f"    Indeed: {len(jobs)} SAP jobs found")
    return jobs

# ── MAIN ─────────────────────────────────────────────────────────────────────

import hashlib

def main():
    sys.stdout.reconfigure(encoding="utf-8")
    print("=" * 60)
    print("  Job Board Auto-Scraper — IIMJobs | Hirist | Instahyre | Indeed")
    print(f"  {datetime.now().strftime('%d %b %Y %H:%M')}")
    print("=" * 60)

    log = load_log()
    all_jobs = []

    for keyword in KEYWORDS:
        print(f"\n  Keyword: {keyword}")
        all_jobs.extend(scrape_iimjobs(keyword))
        all_jobs.extend(scrape_hirist(keyword))
        all_jobs.extend(scrape_instahyre(keyword))
        all_jobs.extend(scrape_indeed(keyword))
        time.sleep(2)

    # Deduplicate by job_id
    seen_ids = set()
    unique_jobs = []
    for job in all_jobs:
        if job["job_id"] not in seen_ids:
            seen_ids.add(job["job_id"])
            unique_jobs.append(job)

    print(f"\n  Total unique SAP jobs found : {len(unique_jobs)}")

    # Filter already applied
    new_jobs = [j for j in unique_jobs if not already_applied(j["job_id"], log)]
    print(f"  New (not yet applied)       : {len(new_jobs)}")

    # Log all new jobs
    now = datetime.now().isoformat()
    for job in new_jobs:
        log.append({
            **job,
            "timestamp": now,
            "status": "logged",
        })
    save_log(log)

    # Print summary table
    print(f"\n  {'Source':<15} {'Title':<45} {'Company':<25}")
    print(f"  {'-'*85}")
    for job in new_jobs[:20]:
        print(f"  {job['source']:<15} {job['title'][:44]:<45} {job['company'][:24]:<25}")

    if len(new_jobs) > 20:
        print(f"  ... and {len(new_jobs) - 20} more (see jobboard_applied_log.json)")

    # Save summary
    by_source = {}
    for j in new_jobs:
        s = j["source"]
        by_source[s] = by_source.get(s, 0) + 1

    summary = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "total_found": len(unique_jobs),
        "new_jobs": len(new_jobs),
        "by_source": by_source,
        "jobs": new_jobs[:50],
    }
    with open(os.path.join(BASE_DIR, "jobboard_summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print(f"\n  By source: {by_source}")
    print(f"  Saved to  : jobboard_applied_log.json")
    print("=" * 60)
    return summary

if __name__ == "__main__":
    main()
