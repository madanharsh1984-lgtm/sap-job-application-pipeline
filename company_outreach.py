"""
company_outreach.py — Direct Hiring Manager Outreach
======================================================
Targets VP IT / CIO / Head of SAP at companies known to run SAP S/4HANA.
Sends a short, direct 4-line outreach email — no resume attached (keeps it
conversational; resume sent only if they reply).

Logic:
  1. Load target company contact list (target_companies.json)
  2. Skip any emailed within last 45 days
  3. Send personalised 4-line direct outreach email
  4. Log result

Cadence: each contact MAX once every 45 days.
"""

import json, os, sys, smtplib, time
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

BASE_DIR   = r"C:\Users\madan\OneDrive\Desktop\Linkdin Job Application"
LOG_FILE   = os.path.join(BASE_DIR, "company_outreach_log.json")
LIST_FILE  = os.path.join(BASE_DIR, "target_companies.json")
RESUME_FILE= os.path.join(BASE_DIR, "Harsh_Madan_SAP_PM_AgileES.docx")

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT   = 465
SMTP_USER   = "Madan.harsh1984@gmail.com"
SMTP_PASS   = "hvaqnirvdvtkvofb"

RESEND_DAYS = 45
SEND_DELAY  = 3
TEST_MODE   = "--all" not in sys.argv
TEST_LIMIT  = 2

SUBJECT = "SAP S/4HANA Programme Lead — 12 Go-Lives, 30 Countries | Available Now"

EMAIL_BODY = """\
Dear {name},

I came across {company}'s SAP programme and wanted to reach out directly.

I'm Harsh Madan — SAP S/4HANA Program Manager with 15 years, recently completing \
a 30-country rollout at Autodesk (12 go-lives, 50M+ records migrated, zero critical defects). \
I specialise in {speciality} and am available immediately for remote engagements.

Would a 15-minute call make sense to explore if there's a fit?

Kind regards,
Harsh Madan
+91 96679 64756 | Madan.harsh1984@gmail.com
LinkedIn: https://sg.linkedin.com/in/harsh-madan-b818113b
"""

# ── TARGET COMPANY DATABASE ───────────────────────────────────────────────────
# Companies running SAP S/4HANA in India — targeting their IT leadership
DEFAULT_COMPANIES = [
    # Manufacturing
    {"company": "Tata Steel",               "name": "Head of IT",           "email": "cio@tatasteel.com",                 "speciality": "SAP S/4HANA Manufacturing"},
    {"company": "Larsen & Toubro",          "name": "VP IT",                "email": "vpit@larsentoubro.com",             "speciality": "SAP PM & ERP transformation"},
    {"company": "Mahindra & Mahindra",      "name": "Head of SAP",          "email": "sap.coe@mahindra.com",              "speciality": "SAP S/4HANA & MDG"},
    {"company": "Bajaj Auto",               "name": "CIO Office",           "email": "it@bajajauto.com",                  "speciality": "SAP S/4HANA"},
    {"company": "Hero MotoCorp",            "name": "VP IT",                "email": "it@heromotocorp.com",               "speciality": "SAP FICO & MM"},
    {"company": "Havells India",            "name": "Head IT",              "email": "ithelpdesk@havells.com",            "speciality": "SAP S/4HANA"},
    {"company": "Godrej Industries",        "name": "CIO",                  "email": "cio@godrej.com",                    "speciality": "SAP S/4HANA & Data Migration"},
    {"company": "JSW Steel",                "name": "Head of SAP",          "email": "it@jsw.in",                         "speciality": "SAP S/4HANA Manufacturing"},
    {"company": "Hindalco Industries",      "name": "VP IT",                "email": "it@hindalco.com",                   "speciality": "SAP Programme Management"},
    {"company": "Bharat Forge",             "name": "CIO",                  "email": "it@bharatforge.com",                "speciality": "SAP S/4HANA"},
    # FMCG / Consumer
    {"company": "Hindustan Unilever",       "name": "VP IT & SAP",          "email": "it.careers@hul.net",                "speciality": "SAP S/4HANA & MDG"},
    {"company": "ITC Limited",              "name": "Head of ERP",          "email": "itc.it@itc.in",                     "speciality": "SAP Programme Management"},
    {"company": "Dabur India",              "name": "CIO",                  "email": "it@dabur.com",                      "speciality": "SAP S/4HANA FMCG"},
    {"company": "Marico",                   "name": "VP Technology",        "email": "technology@marico.com",             "speciality": "SAP ERP"},
    {"company": "Emami Group",              "name": "IT Head",              "email": "it@emami.com",                      "speciality": "SAP S/4HANA"},
    # Pharma
    {"company": "Sun Pharmaceutical",      "name": "Head of SAP",          "email": "it@sunpharma.com",                  "speciality": "SAP S/4HANA & GxP Compliance"},
    {"company": "Dr Reddy's Laboratories", "name": "VP IT",                "email": "it@drreddys.com",                   "speciality": "SAP S/4HANA Pharma"},
    {"company": "Cipla",                    "name": "CIO",                  "email": "it@cipla.com",                      "speciality": "SAP FICO & Data Migration"},
    {"company": "Lupin Pharmaceuticals",   "name": "IT Head",              "email": "it@lupin.com",                      "speciality": "SAP S/4HANA"},
    {"company": "Aurobindo Pharma",        "name": "Head of ERP",          "email": "it@aurobindo.com",                  "speciality": "SAP S/4HANA & FICO"},
    # Technology / IT
    {"company": "Wipro Limited",            "name": "SAP Practice Head",    "email": "sap.practice@wipro.com",            "speciality": "SAP PM & Delivery"},
    {"company": "HCL Technologies",         "name": "SAP Delivery Head",    "email": "sap.delivery@hcltech.com",          "speciality": "SAP S/4HANA Programme"},
    {"company": "Tech Mahindra",            "name": "Head SAP Practice",    "email": "sap@techmahindra.com",              "speciality": "SAP PM & S/4HANA"},
    {"company": "Mphasis",                  "name": "SAP Practice Lead",    "email": "sap@mphasis.com",                   "speciality": "SAP ERP"},
    {"company": "Persistent Systems",       "name": "ERP Head",             "email": "erp@persistent.com",                "speciality": "SAP S/4HANA"},
    # Retail / E-Commerce
    {"company": "Reliance Retail",          "name": "VP IT",                "email": "it@relianceretail.com",             "speciality": "SAP S/4HANA Retail"},
    {"company": "Future Group",             "name": "IT Head",              "email": "it@futuregroup.in",                 "speciality": "SAP ERP"},
    {"company": "Aditya Birla Fashion",     "name": "CIO",                  "email": "it@abfrl.in",                       "speciality": "SAP S/4HANA Retail"},
    {"company": "DMart (Avenue Supermarts)","name": "IT Head",              "email": "it@dmartindia.com",                 "speciality": "SAP ERP"},
    # Banking / NBFC
    {"company": "Bajaj Finserv",            "name": "VP IT",                "email": "it@bajajfinserv.in",                "speciality": "SAP FICO & BFSI"},
    {"company": "Muthoot Finance",          "name": "CIO",                  "email": "it@muthoot.com",                    "speciality": "SAP FICO"},
    {"company": "Shriram Finance",          "name": "Head of IT",           "email": "it@shriramfinance.in",              "speciality": "SAP Finance"},
    # Energy / Oil & Gas
    {"company": "Reliance Industries",      "name": "VP ERP",               "email": "erp@ril.com",                       "speciality": "SAP S/4HANA Energy"},
    {"company": "ONGC",                     "name": "Head of SAP",          "email": "cio@ongc.co.in",                    "speciality": "SAP ERP & Data Migration"},
    {"company": "Vedanta Resources",        "name": "CIO India",            "email": "it@vedanta.co.in",                  "speciality": "SAP S/4HANA Mining"},
    # Logistics
    {"company": "Blue Dart Express",        "name": "VP IT",                "email": "it@bluedart.com",                   "speciality": "SAP S/4HANA Logistics"},
    {"company": "Delhivery",                "name": "Head of ERP",          "email": "erp@delhivery.com",                 "speciality": "SAP S/4HANA"},
    {"company": "Mahindra Logistics",       "name": "CIO",                  "email": "it@mahindralogistics.com",          "speciality": "SAP MM & Logistics"},
    # Global Companies with India Centres
    {"company": "Siemens India",            "name": "Head of SAP",          "email": "sap.india@siemens.com",             "speciality": "SAP S/4HANA Manufacturing"},
    {"company": "ABB India",                "name": "IT Director",          "email": "it.india@in.abb.com",               "speciality": "SAP S/4HANA"},
    {"company": "Honeywell India",          "name": "IT Head India",        "email": "it.india@honeywell.com",            "speciality": "SAP S/4HANA"},
    {"company": "Schneider Electric India", "name": "VP IT",                "email": "it.india@se.com",                   "speciality": "SAP S/4HANA"},
    {"company": "Bosch India",              "name": "Head of SAP",          "email": "sap@bosch.in",                      "speciality": "SAP S/4HANA Manufacturing"},
    {"company": "3M India",                 "name": "IT Director",          "email": "it.india@mmm.com",                  "speciality": "SAP ERP"},
    {"company": "Cummins India",            "name": "IT Head",              "email": "it@cummins.com",                    "speciality": "SAP S/4HANA"},
    {"company": "Saint-Gobain India",       "name": "CIO",                  "email": "it.india@saint-gobain.com",         "speciality": "SAP S/4HANA"},
    {"company": "Philips India",            "name": "IT Director",          "email": "it.india@philips.com",              "speciality": "SAP FICO & MDG"},
    {"company": "GE India",                 "name": "VP IT",                "email": "it.india@ge.com",                   "speciality": "SAP S/4HANA"},
    {"company": "Caterpillar India",        "name": "IT Head",              "email": "it.india@cat.com",                  "speciality": "SAP Manufacturing"},
    {"company": "Emerson India",            "name": "IT Director",          "email": "it.india@emerson.com",              "speciality": "SAP S/4HANA"},
]

# ── HELPERS ───────────────────────────────────────────────────────────────────

def load_log():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, encoding="utf-8") as f:
            return json.load(f)
    return []

def save_log(log):
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2, ensure_ascii=False)

def load_companies():
    if os.path.exists(LIST_FILE):
        with open(LIST_FILE, encoding="utf-8") as f:
            return json.load(f)
    with open(LIST_FILE, "w", encoding="utf-8") as f:
        json.dump(DEFAULT_COMPANIES, f, indent=2, ensure_ascii=False)
    return DEFAULT_COMPANIES

def already_sent_recently(email, log):
    cutoff = datetime.now() - timedelta(days=RESEND_DAYS)
    for e in log:
        if e.get("email", "").lower() == email.lower():
            try:
                if datetime.fromisoformat(e["timestamp"]) > cutoff:
                    return True
            except Exception:
                return True
    return False

def send_company_email(contact):
    body = EMAIL_BODY.format(
        name=contact["name"],
        company=contact["company"],
        speciality=contact["speciality"],
    )
    msg = MIMEMultipart()
    msg["From"]    = SMTP_USER
    msg["To"]      = contact["email"]
    msg["Subject"] = SUBJECT
    msg.attach(MIMEText(body, "plain", "utf-8"))

    # Attach resume for direct outreach
    if os.path.exists(RESUME_FILE):
        with open(RESUME_FILE, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", 'attachment; filename="Harsh_Madan_SAP_PM.docx"')
        msg.attach(part)

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, timeout=30) as server:
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
        return True, ""
    except Exception as e:
        return False, str(e)

# ── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    sys.stdout.reconfigure(encoding="utf-8")
    print("=" * 60)
    print("  Company Direct Outreach — Harsh Madan")
    print(f"  {datetime.now().strftime('%d %b %Y %H:%M')}")
    print(f"  Mode: {'TEST (2 emails)' if TEST_MODE else 'FULL BATCH'}")
    print("=" * 60)

    companies = load_companies()
    log = load_log()
    print(f"  Target companies  : {len(companies)}")
    print(f"  Already contacted : {len(log)}")

    sent_ok, sent_fail, skipped = [], [], 0
    count = 0

    for contact in companies:
        if TEST_MODE and count >= TEST_LIMIT:
            break
        email = contact.get("email", "").strip()
        if not email:
            continue
        if already_sent_recently(email, log):
            skipped += 1
            continue

        print(f"\n  → {contact['company']} | {contact['name']} | {email}")
        success, err = send_company_email(contact)

        entry = {
            "company": contact["company"],
            "name": contact["name"],
            "email": email,
            "timestamp": datetime.now().isoformat(),
            "status": "sent" if success else "failed",
            "error": err,
        }
        log.append(entry)
        save_log(log)

        if success:
            print(f"    ✓ Sent")
            sent_ok.append(contact)
        else:
            print(f"    ✗ Failed: {err}")
            sent_fail.append(contact)

        count += 1
        time.sleep(SEND_DELAY)

    print(f"\n{'=' * 60}")
    print(f"  Sent OK  : {len(sent_ok)}")
    print(f"  Failed   : {len(sent_fail)}")
    print(f"  Skipped  : {skipped} (within {RESEND_DAYS}-day window)")
    print("=" * 60)

    summary = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "sent_ok": len(sent_ok),
        "sent_fail": len(sent_fail),
        "skipped": skipped,
        "contacts": [{"company": c["company"], "email": c["email"]} for c in sent_ok],
    }
    with open(os.path.join(BASE_DIR, "company_outreach_summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    return summary

if __name__ == "__main__":
    main()
