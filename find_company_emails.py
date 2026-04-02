"""
find_company_emails.py — Company HR Email Finder
=================================================
Takes the list of companies from linkedin_posts_today.json (the 79 job records
scraped by brightdata_scrape.py) and finds HR/recruiter email addresses for them.

METHODS (in priority order):
  1. Hunter.io Domain Search API (free: 25 searches/month)
     - Given company name, finds domain, then finds HR/talent/recruiting emails
     - API key: free signup at hunter.io (no credit card)

  2. Company website scrape (free, unlimited)
     - Fetches company website /contact and /careers pages
     - Extracts emails using regex

  3. Hard-coded overrides for well-known SAP staffing companies
     - Common HR email patterns: hr@company.com, careers@company.com, etc.

Output: Updates linkedin_posts_today.json with found emails (has_email=True)
        so that send_sap_emails.py can pick them up and send cold outreach emails.

HOW TO USE:
  1. Sign up free at https://hunter.io → get your API key → paste below
  2. Run: python find_company_emails.py
  3. Then run: python send_sap_emails.py
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

from config import BASE_DIR

# ── CONFIG ─────────────────────────────────────────────────────────────────────
OUTPUT_DIR  = BASE_DIR
JOBS_FILE   = os.path.join(OUTPUT_DIR, "linkedin_posts_today.json")
SENT_LOG    = os.path.join(OUTPUT_DIR, "email_sent_log.json")

# Hunter.io free API key — sign up at https://hunter.io (free, no credit card)
# Free plan: 25 domain searches/month, 25 email finder/month
# Paste your key here after signup:
HUNTER_API_KEY = ""   # e.g. "abc123def456..." — get from hunter.io/api-key

EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}")
SKIP_DOMAINS = {
    "example.com", "domain.com", "email.com", "naukri.com",
    "linkedin.com", "indeed.com", "google.com", "glassdoor.com",
    "sentry.io", "github.com", "microsoft.com", "apple.com",
    "brightdata.com", "sap.com", "w3.org", "schema.org",
}

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}

# ── WELL-KNOWN SAP COMPANY EMAIL PATTERNS ─────────────────────────────────────
# Format: "company name lowercase keyword" -> "known HR email"
KNOWN_EMAILS = {
    "westernacher":     "careers@westernacher.com",
    "digihelic":        "hr@digihelic.com",
    "ntt data":         "india.hr@nttdata.com",
    "capgemini":        "india.careers@capgemini.com",
    "cognizant":        "careersupport@cognizant.com",
    "accenture":        "india.careers@accenture.com",
    "infosys":          "hr@infosys.com",
    "wipro":            "careers@wipro.com",
    "tcs":              "careers@tcs.com",
    "tata consultancy": "careers@tcs.com",
    "hcl":              "india-hr@hcl.com",
    "tech mahindra":    "careers@techmahindra.com",
    "mphasis":          "hr@mphasis.com",
    "hexaware":         "careers@hexaware.com",
    "yash technologies":"recruit@yash.com",
    "lorven":           "careers@lorventech.com",
    "coforge":          "careers@coforge.com",
    "nagarro":          "careers@nagarro.com",
    "fusion consulting": "info@fusion-consulting.com",
    "wms global":       "careers@wmsglobal.com",
    "cube hub":         "hr@cubehubinc.com",
    "delta system":     "careers@deltasss.com",
    "sloka":            "hr@slokaitsolutions.com",
    "tachyon":          "careers@tachyontech.in",
    "syniti":           "careers@syniti.com",
    "kagool":           "careers@kagool.com",
    "weekday":          "hello@weekday.works",
    "droisys":          "careers@droisys.com",
    "rapinno":          "hr@rapinnotech.com",
    "avensys":          "careers@avensysconsulting.com",
    "keylynk":          "hr@keylynk.com",
    "maneva":           "careers@manevagroup.com",
    "blueprint":        "hr@bptl.in",
    "cyan360":          "careers@cyan360.com",
    "rapsys":           "hr@rapsystech.com",
    "kamkon":           "hr@kamkonitsolutions.com",
    "cordiso":          "info@cordiso.com",
    "codem":            "careers@codeminc.com",
    "rayven":           "hr@rayvenitgroup.com",
    "vgreentek":        "hr@vgreentek.com",
    "vgreen":           "hr@vgreentek.com",
    "digitaldhara":     "hr@digitaldhara.com",
    "openiam":          "careers@openiam.com",
    "fullstack":        "jobs@fullstackhq.com",
    "serrala":          "careers@serrala.com",
    "gainwell":         "careers@gainwelltechnologies.com",
    "pwc":              "indiahr@pwc.com",
    "deloitte":         "indiahr@deloitte.com",
    "kpmg":             "india-talent@kpmg.com",
    "ibm":              "careers@in.ibm.com",
    "decskill":         "careers@decskill.com",
    "cortex consultants":"hr@cortexconsultants.com",
    "maitsys":          "contact@maitsys.com",
    "capco":            "india.careers@capco.com",
    "willware":         "hr@willware.com",
    "agilent":          "careers@agilent.com",
    "akamai":           "careers@akamai.com",
}


# ==============================================================================
# HUNTER.IO API (free tier)
# ==============================================================================

def hunter_domain_search(company_name: str) -> list:
    """
    Use Hunter.io to find email addresses for a company.
    Returns list of email strings found.
    """
    if not HUNTER_API_KEY:
        return []

    # First: find the domain
    encoded_name = urllib.parse.quote_plus(company_name)
    url = f"https://api.hunter.io/v2/domain-search?company={encoded_name}&api_key={HUNTER_API_KEY}&limit=5"

    try:
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            emails_data = data.get("data", {}).get("emails", [])
            emails = []
            for e in emails_data:
                addr = e.get("value", "")
                if addr:
                    # Prioritize HR/talent/recruiting emails
                    dept = (e.get("department") or "").lower()
                    seniority = (e.get("seniority") or "").lower()
                    if dept in ("human resources", "recruiting", "talent acquisition") or "hr" in dept:
                        emails.insert(0, addr.lower())
                    else:
                        emails.append(addr.lower())
            return emails
    except Exception as ex:
        print(f"    [Hunter] Error: {ex}")
        return []


# ==============================================================================
# COMPANY WEBSITE EMAIL SCRAPER
# ==============================================================================

def fetch_url(url: str, timeout: int = 10) -> str:
    """Fetch a URL and return HTML text."""
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            charset = resp.headers.get_content_charset() or "utf-8"
            return resp.read().decode(charset, errors="ignore")
    except Exception:
        return ""


def guess_company_domain(company_name: str) -> str:
    """
    Guess the company's website domain from its name.
    Very basic heuristic — replace spaces with hyphens, try .com and .in
    """
    # Clean up
    name = company_name.lower()
    name = re.sub(r'\(.*?\)', '', name).strip()
    name = re.sub(r'pvt\.?\s*ltd\.?|inc\.?|llc\.?|gmbh|pte\.?\s*ltd\.?|limited', '', name, flags=re.IGNORECASE).strip()
    name = re.sub(r'[^a-z0-9 ]', '', name).strip()
    name = name.replace(' ', '')

    return f"https://www.{name}.com"


def scrape_company_emails(company_name: str) -> list:
    """
    Try to find HR emails from company website contact/careers pages.
    """
    domain_url = guess_company_domain(company_name)
    pages_to_try = [
        domain_url + "/contact",
        domain_url + "/careers",
        domain_url + "/contact-us",
        domain_url + "/about",
        domain_url,
    ]

    found = []
    for page_url in pages_to_try[:2]:  # only try first 2 pages per company
        html = fetch_url(page_url, timeout=8)
        if not html:
            continue
        emails = EMAIL_RE.findall(html)
        for e in emails:
            domain = e.split("@")[-1].lower()
            if domain not in SKIP_DOMAINS and len(e) < 80 and "." in domain:
                # Prefer HR/talent emails
                if any(kw in e.lower() for kw in ("hr", "recruit", "career", "talent", "job", "hire")):
                    found.insert(0, e.lower())
                else:
                    found.append(e.lower())
        if found:
            break

    return list(dict.fromkeys(found))[:3]  # max 3 emails per company


# ==============================================================================
# KNOWN EMAIL LOOKUP
# ==============================================================================

def lookup_known_email(company_name: str) -> str:
    """Check hard-coded known emails for this company."""
    name_lower = company_name.lower()
    for keyword, email in KNOWN_EMAILS.items():
        if keyword in name_lower:
            return email
    return ""


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    print("=" * 62)
    print("  Company HR Email Finder")
    print(f"  Date  : {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 62)

    # Load job records
    if not os.path.exists(JOBS_FILE):
        print("  ERROR: linkedin_posts_today.json not found.")
        print("  Run brightdata_scrape.py first.")
        return

    with open(JOBS_FILE, encoding="utf-8") as f:
        records = json.load(f)

    # Load already-sent emails to avoid duplicates
    sent_emails = set()
    if os.path.exists(SENT_LOG):
        try:
            with open(SENT_LOG, encoding="utf-8") as f:
                log = json.load(f)
            sent_emails = {e.get("email", "").lower() for e in log if e.get("email")}
        except Exception:
            pass

    print(f"  Records loaded      : {len(records)}")
    print(f"  Already sent emails : {len(sent_emails)}")
    print(f"  Hunter.io key       : {'SET' if HUNTER_API_KEY else 'NOT SET (known emails only)'}")
    print()

    # Group by company — one email search per company
    company_emails = {}   # company_name -> [email, ...]
    records_without_email = [r for r in records if not r.get("has_email")]

    print(f"  Records without email: {len(records_without_email)}")
    print()

    companies_seen = set()
    companies_to_search = []
    for r in records_without_email:
        company = r.get("company", "").strip()
        if company and company not in companies_seen:
            companies_seen.add(company)
            companies_to_search.append(company)

    print(f"  Unique companies to search: {len(companies_to_search)}")
    print()

    enriched_count = 0

    for i, company in enumerate(companies_to_search):
        print(f"  [{i+1}/{len(companies_to_search)}] {company[:50]}")
        emails = []

        # Method 1: Known email lookup (instant)
        known = lookup_known_email(company)
        if known and known not in sent_emails:
            print(f"    [Known] {known}")
            emails = [known]
        else:
            # Method 2: Hunter.io (if key set)
            if HUNTER_API_KEY:
                hunter_emails = hunter_domain_search(company)
                if hunter_emails:
                    emails = [e for e in hunter_emails if e not in sent_emails]
                    if emails:
                        print(f"    [Hunter] {emails[0]}")
                    time.sleep(1)  # rate limit

            # Method 3: Website scrape (fallback, slower)
            if not emails:
                scraped = scrape_company_emails(company)
                emails = [e for e in scraped if e not in sent_emails]
                if emails:
                    print(f"    [Web] {emails[0]}")

        if not emails:
            print(f"    [--] No email found")
            continue

        # Update all records for this company with the found email
        best_email = emails[0]
        for r in records:
            if r.get("company") == company and not r.get("has_email"):
                r["email"] = best_email
                r["has_email"] = True
                r["email_source"] = "company_lookup"
                enriched_count += 1
                break  # only update first matching record per company

        company_emails[company] = best_email

    # Save enriched records
    with open(JOBS_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)

    # Also update the Temp copy
    try:
        temp_file = r"C:\Users\madan\AppData\Local\Temp\linkedin_posts_today.json"
        with open(temp_file, "w", encoding="utf-8") as f:
            json.dump(records, f, indent=2, ensure_ascii=False)
    except Exception:
        pass

    print()
    print("=" * 62)
    print(f"  Companies searched  : {len(companies_to_search)}")
    print(f"  Emails found        : {len(company_emails)}")
    print(f"  Records enriched    : {enriched_count}")
    print(f"  Saved to            : {JOBS_FILE}")
    print("=" * 62)

    if company_emails:
        print("\n  Email leads ready for cold outreach:")
        for company, email in list(company_emails.items())[:20]:
            print(f"    {email:40s} | {company[:30]}")

    total_with_email = sum(1 for r in records if r.get("has_email"))
    print(f"\n  Total records with email: {total_with_email}")
    print(f"  Run send_sap_emails.py to send cold outreach emails.")


if __name__ == "__main__":
    main()
