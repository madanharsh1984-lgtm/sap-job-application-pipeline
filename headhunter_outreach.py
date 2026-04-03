"""
headhunter_outreach.py — Executive Search Firm Outreach
=========================================================
Sends personalised emails to SAP/ERP recruiters at 50 top
executive search & staffing firms in India + global.

Logic:
  1. Load headhunter contact list (headhunters.json)
  2. Skip any already emailed (headhunter_sent_log.json)
  3. Build tailored resume via resume_builder
  4. Send email with resume attached
  5. Log result

Run daily — only contacts NOT previously reached are emailed.
Cadence: each contact is emailed MAX once every 30 days.
"""

import json, os, sys, smtplib, time
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
sys.path.insert(0, r"C:\Users\madan\OneDrive\Desktop\Linkdin Job Application")
import resume_builder

# ── CONFIG ───────────────────────────────────────────────────────────────────
BASE_DIR   = r"C:\Users\madan\OneDrive\Desktop\Linkdin Job Application"
LOG_FILE   = os.path.join(BASE_DIR, "headhunter_sent_log.json")
LIST_FILE  = os.path.join(BASE_DIR, "headhunters.json")
RESUME_BASE= os.path.join(BASE_DIR, "Harsh_Madan_SAP_PM_AgileES.docx")

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT   = 465
SMTP_USER   = "Madan.harsh1984@gmail.com"
SMTP_PASS   = "hvaqnirvdvtkvofb"

RESEND_DAYS = 30   # don't re-email same person within 30 days
SEND_DELAY  = 3    # seconds between emails
TEST_MODE   = "--all" not in sys.argv
TEST_LIMIT  = 2

SUBJECT = "Senior SAP S/4HANA Program Manager — Available Immediately | 15+ Years | Remote"

EMAIL_BODY = """\
Dear {name},

I am writing to register my profile with {firm} for senior SAP opportunities.

I am Harsh Madan, a SAP S/4HANA Program Manager with 15+ years of experience \
delivering large-scale ERP transformations. I have recently completed a 30-country \
S/4HANA rollout at Autodesk, leading a PMO of 80+ consultants with 12 global \
go-lives — all on time, zero critical defects.

Key highlights:
• 50M+ records migrated (LTMC, LSMW, SLT, SAP CPI) — 100% reconciliation accuracy
• 97% UAT first-pass rate across 1,200+ test scripts (FICO, MM, SD, MDG)
• ₹4 Cr annual savings via SAP MDG master data governance implementation
• 12 global S/4HANA go-lives across 30 countries — Manufacturing, Technology, FMCG

Current status:
• Available: Immediately
• Preferred: Remote (open to hybrid)
• Expected CTC: ₹40 LPA
• Modules: FICO, MM, SD, MDG, Data Migration (LSMW/LTMC/SLT/CPI)

I have attached my resume for your consideration. I would welcome the opportunity \
to discuss any relevant mandates you may be working on.

Kind regards,
Harsh Madan
+91 96679 64756
Madan.harsh1984@gmail.com
LinkedIn: https://sg.linkedin.com/in/harsh-madan-b818113b
"""

# ── HEADHUNTER DATABASE ───────────────────────────────────────────────────────
# 50 executive search & staffing firms — SAP/ERP practice contacts
DEFAULT_HEADHUNTERS = [
    # Big Staffing — India SAP Practice
    {"firm": "Michael Page India",         "name": "SAP Practice Team",    "email": "it.india@michaelpage.co.in",        "speciality": "SAP PM"},
    {"firm": "Randstad India",             "name": "IT Staffing Team",     "email": "it@randstad.in",                    "speciality": "SAP"},
    {"firm": "Adecco India",               "name": "Technology Division",  "email": "technology@adecco.com",             "speciality": "ERP"},
    {"firm": "Manpower Group India",       "name": "IT Practice",          "email": "india@manpowergroup.com",           "speciality": "SAP"},
    {"firm": "Quess Corp",                 "name": "IT Staffing",          "email": "itrecruitment@quesscorp.com",       "speciality": "SAP"},
    {"firm": "TeamLease IT",               "name": "Technology Team",      "email": "it@teamlease.com",                  "speciality": "ERP"},
    {"firm": "Xpheno",                     "name": "SAP Recruitment",      "email": "careers@xpheno.com",                "speciality": "SAP"},
    {"firm": "Antal International India",  "name": "Technology Practice",  "email": "india@antal.com",                   "speciality": "SAP PM"},
    {"firm": "Spectrum Talent Management", "name": "SAP Practice",         "email": "saprecruit@spectrumtalent.in",      "speciality": "SAP"},
    {"firm": "ABC Consultants",            "name": "IT Practice Head",     "email": "it@abcconsultants.in",              "speciality": "SAP"},
    {"firm": "Mafoi Management",           "name": "Technology Division",  "email": "technology@mafoi.com",              "speciality": "ERP"},
    {"firm": "Ma Foi Randstad",            "name": "IT Team",              "email": "it.staffing@mafoirandstad.com",     "speciality": "SAP"},
    {"firm": "Korn Ferry India",           "name": "Technology Practice",  "email": "india@kornferry.com",               "speciality": "CIO/VP IT"},
    {"firm": "Spencer Stuart India",       "name": "Technology Practice",  "email": "delhi@spencerstuart.com",           "speciality": "Executive SAP"},
    {"firm": "Egon Zehnder India",         "name": "Technology Practice",  "email": "delhi@egonzehnder.com",             "speciality": "Executive"},
    # SAP-Specific Recruiters India
    {"firm": "ITC Infotech HR",            "name": "SAP Talent Team",      "email": "saptalent@itcinfotech.com",         "speciality": "SAP"},
    {"firm": "Birlasoft HR",               "name": "SAP Practice HR",      "email": "careers@birlasoft.com",             "speciality": "SAP PM"},
    {"firm": "Yash Technologies HR",       "name": "SAP Hiring",           "email": "hr@yashtechnologies.com",           "speciality": "SAP"},
    {"firm": "Sonata Software HR",         "name": "SAP Practice",         "email": "careers@sonata-software.com",       "speciality": "SAP"},
    {"firm": "Kellton Tech HR",            "name": "SAP Team",             "email": "hr@kelltontech.com",                "speciality": "SAP"},
    {"firm": "Mastech Digital",            "name": "SAP Staffing",         "email": "sap@mastechdigital.com",            "speciality": "SAP"},
    {"firm": "Nihilent HR",                "name": "SAP Practice",         "email": "hr@nihilent.com",                   "speciality": "SAP PM"},
    {"firm": "KPIT Technologies HR",       "name": "SAP Team",             "email": "careers@kpit.com",                  "speciality": "SAP"},
    {"firm": "Hexaware HR",                "name": "SAP Talent",           "email": "careers@hexaware.com",              "speciality": "SAP"},
    {"firm": "Mphasis HR",                 "name": "ERP Team",             "email": "careers@mphasis.com",               "speciality": "SAP"},
    # Global SAP Staffing
    {"firm": "Allegis Group",              "name": "SAP Practice",         "email": "sap@allegisgroup.com",              "speciality": "Global SAP"},
    {"firm": "NTT Data HR India",          "name": "SAP Team",             "email": "careers.india@nttdata.com",         "speciality": "SAP"},
    {"firm": "DXC Technology HR",          "name": "SAP Practice",         "email": "india.careers@dxc.com",             "speciality": "SAP"},
    {"firm": "Cognizant SAP Practice HR",  "name": "SAP Hiring",           "email": "sap.careers@cognizant.com",         "speciality": "SAP PM"},
    {"firm": "Capgemini SAP HR India",     "name": "SAP Talent",           "email": "sap.india@capgemini.com",           "speciality": "SAP"},
    # Niche Executive Search
    {"firm": "GreenHouse HR",              "name": "ERP Practice",         "email": "erp@greenhouse-hr.com",             "speciality": "SAP"},
    {"firm": "Talent Leads HR",            "name": "SAP Team",             "email": "sap@talentleadshr.com",             "speciality": "SAP"},
    {"firm": "Ikon Consultants",           "name": "IT Division",          "email": "it@ikonconsultants.com",            "speciality": "SAP"},
    {"firm": "Iris Corporate Solutions",   "name": "SAP Practice",         "email": "sap@iriscorporate.com",             "speciality": "SAP PM"},
    {"firm": "Futurz Staffing",            "name": "Technology Team",      "email": "technology@futurzstaffing.com",     "speciality": "ERP"},
    {"firm": "Synergy Consultants",        "name": "SAP Team",             "email": "sap@synergyconsultants.in",         "speciality": "SAP"},
    {"firm": "Hays India",                 "name": "IT Practice",          "email": "india@hays.com",                    "speciality": "SAP PM"},
    {"firm": "Robert Walters India",       "name": "Technology Division",  "email": "india@robertwalters.com",           "speciality": "SAP"},
    {"firm": "Hudson RPO India",           "name": "ERP Team",             "email": "india@hudson.com",                  "speciality": "SAP"},
    {"firm": "Gi Group India",             "name": "IT Staffing",          "email": "it@gigroup.co.in",                  "speciality": "SAP"},
    # Gulf / Singapore (Remote from India)
    {"firm": "GulfTalent (UAE)",           "name": "SAP Practice",         "email": "sap@gulftalent.com",                "speciality": "SAP Gulf"},
    {"firm": "Bayt.com UAE",               "name": "Technology Team",      "email": "technology@bayt.com",               "speciality": "SAP UAE"},
    {"firm": "Mindfield Resources",        "name": "APAC SAP Team",        "email": "sap@mindfieldresources.com",        "speciality": "SAP APAC"},
    {"firm": "RecruitFirst Singapore",     "name": "SAP Team",             "email": "sap@recruitfirst.co",               "speciality": "SAP Singapore"},
    {"firm": "Hudson Singapore",           "name": "Technology Practice",  "email": "singapore@hudson.com",              "speciality": "SAP SG"},
    # UK Remote
    {"firm": "Harvey Nash UK",             "name": "SAP Practice",         "email": "sap@harveynash.com",                "speciality": "SAP UK"},
    {"firm": "Lorien Resourcing UK",       "name": "ERP Team",             "email": "sap@lorienresourcing.com",          "speciality": "SAP UK"},
    {"firm": "Huxley Associates UK",       "name": "SAP Team",             "email": "sap@huxley.com",                    "speciality": "SAP UK"},
    {"firm": "Roc Search UK",              "name": "SAP Practice",         "email": "sap@rocsearch.com",                 "speciality": "SAP UK"},
    {"firm": "Experis IT UK",              "name": "SAP Team",             "email": "sap@experis.co.uk",                 "speciality": "SAP UK"},
]

# ── HELPERS ───────────────────────────────────────────────────────────────────

def load_log() -> list:
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, encoding="utf-8") as f:
            return json.load(f)
    return []

def save_log(log: list):
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2, ensure_ascii=False)

def load_headhunters() -> list:
    """Load from file if exists, else use default list."""
    if os.path.exists(LIST_FILE):
        with open(LIST_FILE, encoding="utf-8") as f:
            return json.load(f)
    # Save default list for future editing
    with open(LIST_FILE, "w", encoding="utf-8") as f:
        json.dump(DEFAULT_HEADHUNTERS, f, indent=2, ensure_ascii=False)
    return DEFAULT_HEADHUNTERS

def already_sent_recently(email: str, log: list) -> bool:
    cutoff = datetime.now() - timedelta(days=RESEND_DAYS)
    for entry in log:
        if entry.get("email", "").lower() == email.lower():
            try:
                sent_date = datetime.fromisoformat(entry["timestamp"])
                if sent_date > cutoff:
                    return True
            except Exception:
                return True  # be safe, skip
    return False

def send_headhunter_email(contact: dict) -> tuple:
    """Build tailored resume + send email. Returns (success, error)."""
    # Build a generic SAP PM post for resume_builder
    fake_post = {
        "full_post_text": (
            f"Looking for SAP S/4HANA Program Manager with data migration experience. "
            f"FICO MM SD MDG LSMW LTMC SLT SAP CPI cutover planning UAT SIT PMO. "
            f"Remote. {contact['speciality']}"
        ),
        "company": contact["firm"],
        "email": contact["email"],
        "recruiter_name": contact["name"],
        "search_keyword": {"search": "SAP S4 HANA Project Manager"},
    }

    resume_path = None
    try:
        resume_path = resume_builder.generate(fake_post)
    except Exception as e:
        resume_path = RESUME_BASE
        print(f"    [resume fallback: {e}]")

    body = EMAIL_BODY.format(name=contact["name"], firm=contact["firm"])

    msg = MIMEMultipart()
    msg["From"]    = SMTP_USER
    msg["To"]      = contact["email"]
    msg["Subject"] = SUBJECT
    msg.attach(MIMEText(body, "plain", "utf-8"))

    if resume_path and os.path.exists(resume_path):
        with open(resume_path, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", 'attachment; filename="Harsh_Madan_SAP_PM.docx"')
        msg.attach(part)

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, timeout=30) as server:
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
        result = (True, "")
    except Exception as e:
        result = (False, str(e))

    # Cleanup temp resume
    try:
        if resume_path and resume_path != RESUME_BASE and os.path.exists(resume_path):
            os.remove(resume_path)
    except Exception:
        pass

    return result

# ── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    sys.stdout.reconfigure(encoding="utf-8")
    print("=" * 60)
    print("  Headhunter Outreach — Harsh Madan")
    print(f"  {datetime.now().strftime('%d %b %Y %H:%M')}")
    print(f"  Mode: {'TEST (2 emails)' if TEST_MODE else 'FULL BATCH'}")
    print("=" * 60)

    headhunters = load_headhunters()
    log = load_log()
    print(f"  Total headhunter contacts : {len(headhunters)}")
    print(f"  Previously contacted      : {len(log)}")

    sent_ok, sent_fail, skipped = [], [], 0
    count = 0

    for contact in headhunters:
        if TEST_MODE and count >= TEST_LIMIT:
            break

        email = contact.get("email", "").strip()
        if not email:
            continue

        if already_sent_recently(email, log):
            skipped += 1
            continue

        print(f"\n  → {contact['firm']} | {contact['name']} | {email}")
        success, err = send_headhunter_email(contact)

        entry = {
            "firm": contact["firm"],
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
            sent_fail.append({"contact": contact, "error": err})

        count += 1
        time.sleep(SEND_DELAY)

    print(f"\n{'=' * 60}")
    print(f"  Sent OK  : {len(sent_ok)}")
    print(f"  Failed   : {len(sent_fail)}")
    print(f"  Skipped  : {skipped} (already contacted within {RESEND_DAYS} days)")
    print("=" * 60)

    # Save summary
    summary = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "sent_ok": len(sent_ok),
        "sent_fail": len(sent_fail),
        "skipped": skipped,
        "contacts": [{"firm": c["firm"], "email": c["email"]} for c in sent_ok],
    }
    with open(os.path.join(BASE_DIR, "headhunter_summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    return summary

if __name__ == "__main__":
    main()
