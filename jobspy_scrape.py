"""
STEP 1 — LinkedIn Post Scraper (JobSpy Edition)
================================================
Replaces Apify harvestapi~linkedin-post-search with the FREE JobSpy library.

JobSpy (python-jobspy) — 100% free, no API key, no credits.
GitHub: https://github.com/speedyapply/JobSpy
Install: pip install python-jobspy

Searches LinkedIn Jobs (+ Indeed + Google as bonus sources) for 4 SAP titles,
extracts recruiter emails from job descriptions, and saves:
  - linkedin_posts_today.json   (same format as before — pipeline compatible)
  - email_sent_log.json         (reset check handled in send_emails.py)
"""

import json, re, os, sys
from datetime import datetime
from config import BASE_DIR, JOB_TITLES

OUTPUT_DIR  = BASE_DIR
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "linkedin_posts_today.json")

# Email regex
EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}")

def scrape_with_jobspy():
    try:
        from jobspy import scrape_jobs
    except ImportError:
        print("ERROR: python-jobspy not installed.")
        print("Please double-click Install_JobSpy.bat first, then re-run this script.")
        sys.exit(1)

    all_results = []
    seen_urls   = set()

    for title in JOB_TITLES:
        print(f"\nSearching: {title}")
        try:
            jobs = scrape_jobs(
                site_name=["linkedin", "indeed", "google"],
                search_term=title,
                location="India",
                results_wanted=50,
                hours_old=24,
                is_remote=True,
                linkedin_fetch_description=True,  # get full description for email extraction
            )
            print(f"  Found {len(jobs)} jobs")

            for _, row in jobs.iterrows():
                job_url = str(row.get("job_url", ""))
                if job_url in seen_urls:
                    continue
                seen_urls.add(job_url)

                # Build description blob for email search
                description = str(row.get("description", "") or "")
                title_text  = str(row.get("title", "") or "")
                company     = str(row.get("company", "") or "")
                recruiter   = str(row.get("company", "") or "")  # JobSpy doesn't expose recruiter name separately

                # Extract emails from description
                emails = EMAIL_RE.findall(description)
                # Filter out common false-positives (image filenames, privacy emails, etc.)
                skip_domains = {"example.com", "domain.com", "email.com", "naukri.com",
                                "linkedin.com", "indeed.com", "google.com", "glassdoor.com"}
                valid_emails = [
                    e for e in emails
                    if not any(d in e.lower() for d in skip_domains)
                    and len(e) < 80
                ]
                email = valid_emails[0] if valid_emails else ""

                all_results.append({
                    "recruiter_name": recruiter,
                    "company":        company,
                    "email":          email,
                    "has_email":      bool(email),
                    "full_post_text": description,
                    "post_url":       job_url,
                    "posted_at":      str(row.get("date_posted", "")),
                    "job_title":      title_text,
                    "location":       str(row.get("location", "")),
                    "source":         str(row.get("site", "")),
                    "search_keyword": title,
                })

        except Exception as e:
            print(f"  ERROR for '{title}': {e}")

    return all_results


def main():
    print("=" * 55)
    print("  STEP 1 — JobSpy LinkedIn Scraper (Free / No Credits)")
    print("  Date:", datetime.now().strftime("%Y-%m-%d %H:%M"))
    print("=" * 55)

    results = scrape_with_jobspy()

    # Deduplicate by URL
    seen = set()
    unique = []
    for r in results:
        k = r["post_url"]
        if k not in seen:
            seen.add(k)
            unique.append(r)

    with_email = [r for r in unique if r["has_email"]]

    # Save output
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(unique, f, indent=2, ensure_ascii=False)

    # Also save a copy in Temp for cron pipeline
    temp_file = r"C:\Users\madan\AppData\Local\Temp\linkedin_posts_today.json"
    with open(temp_file, "w", encoding="utf-8") as f:
        json.dump(unique, f, indent=2, ensure_ascii=False)

    print(f"\n{'='*55}")
    print(f"  Total jobs found : {len(unique)}")
    print(f"  With email       : {len(with_email)}")
    print(f"  Saved to         : {OUTPUT_FILE}")
    print(f"{'='*55}")

    if with_email:
        print("\n  Email leads found:")
        for r in with_email:
            print(f"    {r['email']:40s} | {r['company'][:30]}")

    # Save summary
    summary = {
        "date":          datetime.now().strftime("%Y-%m-%d"),
        "total_found":   len(unique),
        "with_email":    len(with_email),
        "per_keyword":   {},
    }
    for t in JOB_TITLES:
        summary["per_keyword"][t] = len([r for r in unique if r.get("search_keyword") == t])

    summary_file = os.path.join(OUTPUT_DIR, "jobspy_summary.json")
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print(f"\n  Summary saved to : {summary_file}")
    return unique


if __name__ == "__main__":
    main()
