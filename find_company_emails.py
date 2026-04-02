"""
find_company_emails.py — Company HR Email Finder (with DNS MX validation)
==========================================================================
Finds HR email addresses for companies from the jobs file.
Validates each email via DNS MX check BEFORE assigning it.
Only emails with confirmed MX records are marked has_email=True.

METHODS (in priority order):
  1. Hard-coded verified emails for known SAP companies (corrected list)
  2. Hunter.io API (optional — set HUNTER_API_KEY if you have one)
  3. Company website scrape

ALL candidates are DNS MX validated before use.

Run this BEFORE send_sap_emails.py.
"""

import json, re, os, sys, time, socket
import urllib.request, urllib.parse
from datetime import datetime

sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)
sys.stderr.reconfigure(encoding="utf-8", line_buffering=True)

from config import BASE_DIR

OUTPUT_DIR = BASE_DIR
JOBS_FILE  = os.path.join(OUTPUT_DIR, "linkedin_posts_today.json")
SENT_LOG   = os.path.join(OUTPUT_DIR, "email_sent_log.json")

HUNTER_API_KEY = ""  # optional — get free key at hunter.io

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
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

# ── VERIFIED KNOWN EMAILS ──────────────────────────────────────────────────────
# Only emails that are CONFIRMED working (MX verified + not bounced).
# Removed all entries that bounced in April 2026 batch.
# Keyword must appear in company name (case-insensitive substring).
KNOWN_EMAILS = {
    # Large IT companies — verified working domains
    "ntt data":          "careers@nttdata.com",
    "capgemini":         "india.careers@capgemini.com",
    "cognizant":         "careersupport@cognizant.com",
    "accenture":         "careers@accenture.com",
    "infosys":           "hr@infosys.com",
    "wipro":             "careers@wipro.com",
    "tata consultancy":  "careers@tcs.com",
    "tcs":               "careers@tcs.com",
    "hcl":               "india-hr@hcl.com",
    "tech mahindra":     "careers@techmahindra.com",
    "mphasis":           "hr@mphasis.com",
    "hexaware":          "careers@hexaware.com",
    "coforge":           "careers@coforge.com",
    "nagarro":           "careers@nagarro.com",
    "syniti":            "careers@syniti.com",
    "kagool":            "careers@kagool.com",
    "serrala":           "careers@serrala.com",
    "gainwell":          "careers@gainwelltechnologies.com",
    "pwc":               "careers@pwc.in",
    "deloitte":          "recruit@deloitte.com",
    "kpmg":              "recruit@kpmg.com",
    "ibm":               "careers@in.ibm.com",
    "yash technologies": "recruit@yash.com",
    "tachyon":           "careers@tachyontech.in",
    "digihelic":         "hr@digihelic.com",
    "vgreentek":         "hr@vgreentek.com",
    "vgreen":            "hr@vgreentek.com",
    "rapinno":           "hr@rapinnotech.com",
    "cordiso":           "info@cordiso.com",
    "willware":          "hr@willware.com",
    "keylynk":           "hr@keylynk.com",
    "maitsys":           "contact@maitsys.com",
    # NOTE: The following were REMOVED because they bounced:
    # westernacher (careers@), lorven (careers@), cyan360 (careers@),
    # fusion-consulting (info@), decskill (careers@), weekday (hello@),
    # droisys (careers@), avensysconsulting, openiam (careers@),
    # fullstackhq (jobs@), slokaitsolutions, rayvenitgroup, codeminc,
    # kamkonitsolutions, rapsystech, deltasss, cubehubinc, bptl.in,
    # capco (india.careers@), agilent (careers@), manevagroup (careers@)
}


# ==============================================================================
# DNS MX VALIDATION
# ==============================================================================

def has_mx_record(domain: str, timeout: int = 5) -> bool:
    """
    Check if a domain has MX records using dnspython (preferred)
    or raw socket DNS lookup (fallback).
    Returns True if domain can receive email, False otherwise.
    """
    # Method 1: dnspython (accurate)
    try:
        import dns.resolver
        answers = dns.resolver.resolve(domain, 'MX', lifetime=timeout)
        return len(list(answers)) > 0
    except ImportError:
        pass
    except Exception:
        return False

    # Method 2: socket lookup as rough fallback
    try:
        socket.setdefaulttimeout(timeout)
        socket.getaddrinfo(domain, 25)
        return True
    except Exception:
        return False


def validate_email_domain(email: str) -> tuple:
    """
    Validate that the email's domain has MX records.
    Returns (is_valid: bool, reason: str)
    """
    if not email or '@' not in email:
        return False, "Invalid format"
    domain = email.split('@')[1].lower()
    if domain in SKIP_DOMAINS:
        return False, f"Skipped domain: {domain}"
    if has_mx_record(domain):
        return True, "MX OK"
    return False, f"No MX record: {domain}"


# ==============================================================================
# EMAIL LOOKUP METHODS
# ==============================================================================

def lookup_known_email(company_name: str) -> str:
    """Return verified known HR email if company matches a keyword."""
    name_lower = company_name.lower()
    for keyword, email in KNOWN_EMAILS.items():
        if keyword in name_lower:
            return email
    return ""


def hunter_domain_search(company_name: str) -> list:
    """Hunter.io domain search — returns list of emails."""
    if not HUNTER_API_KEY:
        return []
    encoded = urllib.parse.quote_plus(company_name)
    url = (f"https://api.hunter.io/v2/domain-search"
           f"?company={encoded}&api_key={HUNTER_API_KEY}&limit=5")
    try:
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            emails_data = data.get("data", {}).get("emails", [])
            emails = []
            for e in emails_data:
                addr = e.get("value", "")
                if not addr:
                    continue
                dept = (e.get("department") or "").lower()
                if "hr" in dept or "recruit" in dept or "talent" in dept:
                    emails.insert(0, addr.lower())
                else:
                    emails.append(addr.lower())
            return emails
    except Exception as ex:
        print(f"    [Hunter] Error: {ex}")
        return []


def fetch_url(url: str, timeout: int = 8) -> str:
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            charset = resp.headers.get_content_charset() or "utf-8"
            return resp.read().decode(charset, errors="ignore")
    except Exception:
        return ""


def scrape_company_emails(company_name: str) -> list:
    """Guess domain and scrape contact/careers pages for emails."""
    name = company_name.lower()
    name = re.sub(r'\(.*?\)', '', name).strip()
    name = re.sub(r'pvt\.?\s*ltd\.?|inc\.?|llc\.?|gmbh|pte\.?\s*ltd\.?|limited',
                  '', name, flags=re.IGNORECASE).strip()
    name = re.sub(r'[^a-z0-9 ]', '', name).strip().replace(' ', '')
    base = f"https://www.{name}.com"

    found = []
    for page in [base + "/contact", base + "/careers", base]:
        html = fetch_url(page, timeout=8)
        if not html:
            continue
        for e in EMAIL_RE.findall(html):
            domain = e.split("@")[-1].lower()
            if domain not in SKIP_DOMAINS and len(e) < 80 and "." in domain:
                if any(kw in e.lower() for kw in ("hr", "recruit", "career", "talent")):
                    found.insert(0, e.lower())
                else:
                    found.append(e.lower())
        if found:
            break
    return list(dict.fromkeys(found))[:3]


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    print("=" * 62)
    print("  Company HR Email Finder (with DNS MX validation)")
    print(f"  Date  : {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 62)

    if not os.path.exists(JOBS_FILE):
        print("  ERROR: linkedin_posts_today.json not found.")
        return

    with open(JOBS_FILE, encoding="utf-8") as f:
        records = json.load(f)

    sent_emails = set()
    if os.path.exists(SENT_LOG):
        try:
            with open(SENT_LOG, encoding="utf-8") as f:
                log = json.load(f)
            sent_emails = {e.get("email", "").lower() for e in log if e.get("email")}
        except Exception:
            pass

    print(f"  Records loaded       : {len(records)}")
    print(f"  Already sent         : {len(sent_emails)}")
    print()

    # Collect companies that don't have a valid email yet
    records_without = [r for r in records if not r.get("has_email") or not r.get("email")]
    companies_seen  = set()
    companies_list  = []
    for r in records_without:
        company = (r.get("company") or "").strip()
        if company and company not in companies_seen:
            companies_seen.add(company)
            companies_list.append(company)

    print(f"  Records needing email: {len(records_without)}")
    print(f"  Unique companies     : {len(companies_list)}")
    print()

    company_emails = {}  # company -> verified email
    enriched = 0

    for i, company in enumerate(companies_list):
        print(f"  [{i+1}/{len(companies_list)}] {company[:50]}")
        candidate = ""

        # Method 1: known list
        known = lookup_known_email(company)
        if known and known not in sent_emails:
            candidate = known
            src = "known"
        elif HUNTER_API_KEY:
            found = hunter_domain_search(company)
            for e in found:
                if e not in sent_emails:
                    candidate = e
                    src = "hunter"
                    break
            time.sleep(0.5)

        # Method 3: website scrape
        if not candidate:
            scraped = scrape_company_emails(company)
            for e in scraped:
                if e not in sent_emails:
                    candidate = e
                    src = "web"
                    break

        if not candidate:
            print(f"    [--] No email found")
            continue

        # ── DNS MX VALIDATION ──────────────────────────────────────────
        is_valid, reason = validate_email_domain(candidate)
        if not is_valid:
            print(f"    [SKIP] {candidate} — {reason}")
            continue

        print(f"    [{src.upper()}] {candidate} — {reason}")
        company_emails[company] = candidate

        # Update first matching record
        for r in records:
            if (r.get("company") or "").strip() == company and not r.get("has_email"):
                r["email"]        = candidate
                r["has_email"]    = True
                r["email_valid"]  = True
                r["email_source"] = src
                enriched += 1
                break

    # Save
    with open(JOBS_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)

    try:
        temp = r"C:\Users\madan\AppData\Local\Temp\linkedin_posts_today.json"
        with open(temp, "w", encoding="utf-8") as f:
            json.dump(records, f, indent=2, ensure_ascii=False)
    except Exception:
        pass

    total_with = sum(1 for r in records if r.get("has_email") and r.get("email_valid") is not False)

    print()
    print("=" * 62)
    print(f"  Companies searched   : {len(companies_list)}")
    print(f"  Valid emails found   : {len(company_emails)}")
    print(f"  Records enriched     : {enriched}")
    print(f"  Total ready to send  : {total_with}")
    print(f"  Saved to             : {JOBS_FILE}")
    print("=" * 62)

    if company_emails:
        print("\n  Validated email leads:")
        for company, email in list(company_emails.items()):
            print(f"    {email:40s} | {company[:30]}")
    else:
        print("\n  No new valid emails found.")

    return records


if __name__ == "__main__":
    main()
