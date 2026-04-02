"""
send_sap_emails.py — SAP Job Application Email Sender
======================================================
Sends personalised cold-outreach emails to HR/recruiters found in
linkedin_posts_today.json.

SAFETY FEATURES:
  1. DNS MX validation — skip emails whose domain has no MX record
  2. Test-3-first mode — by default sends only the first 3 emails,
     waits for manual confirmation before sending the rest.
     Set TEST_MODE = False to send all in one shot (e.g. once confirmed).
  3. Duplicate guard — tracks sent emails in email_sent_log.json
  4. Per-email error handling — one bad address doesn't stop the batch

HOW TO USE:
  First run  : python send_sap_emails.py          (sends first 3 — check inbox)
  Full batch : python send_sap_emails.py --all    (sends all remaining)
"""

import json, smtplib, os, sys, socket, time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
import resume_builder

sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)
sys.stderr.reconfigure(encoding="utf-8", line_buffering=True)

from config import SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASS, BASE_DIR, LOG_DIR

POSTS_FILE   = os.path.join(BASE_DIR, "linkedin_posts_today.json")
LOG_FILE     = os.path.join(LOG_DIR,  "email_sent_log.json")
RESUME_FILE  = os.path.join(BASE_DIR, "Harsh_Madan_SAP_PM_AgileES.docx")
RESUME_NAME  = "Harsh_Madan_SAP_PM.docx"   # filename shown to recipient

# --all flag → full batch; default → test 3 only
TEST_MODE   = "--all" not in sys.argv
TEST_LIMIT  = 3  # how many to send in test mode

SEND_DELAY  = 2   # seconds between emails (2s is enough; 5s was too slow)

# ── EMAIL TEMPLATE ─────────────────────────────────────────────────────────────
EMAIL_SUBJECT  = "Application – SAP S/4HANA Program Manager / Data Migration Specialist"

EMAIL_BODY = """\
Dear {recruiter_name},

I came across {company_ref}and wanted to reach out regarding SAP opportunities you may be hiring for.

I am Harsh Madan, a SAP S/4HANA Program Manager with 15+ years of end-to-end SAP implementation experience across ECC and S/4HANA environments. Key highlights:

• SAP S/4HANA Program Manager at Autodesk (May 2015–Present) — led full-cycle ECC to S/4HANA migrations
• Expert in Data Migration: LSMW, LTMC, SLT, SAP CPI — managed 10M+ record migrations with zero data loss
• Modules: FICO, MM, SD, MDG — cross-functional alignment across Finance, Procurement, and Sales
• Cutover Planning, SIT/UAT, Stakeholder Management — delivered on-time, zero critical post-go-live defects
• Tools: SAP Solution Manager, JIRA, Smartsheet, SAP MDG

Current CTC: 35 LPA | Expected: 40 LPA | Notice Period: Immediate
Open to: Remote / Hybrid roles across India

I would love to connect and discuss how my profile aligns with your current requirements. Please feel free to reach out or share any relevant JDs.

Kind regards,
Harsh Madan
+91 96679 64756
Madan.harsh1984@gmail.com
LinkedIn: https://sg.linkedin.com/in/harsh-madan-b818113b\
"""


# ==============================================================================
# DNS MX VALIDATION
# ==============================================================================

def has_mx_record(domain: str, timeout: int = 5) -> bool:
    """Return True if domain has MX records (can receive email)."""
    try:
        import dns.resolver
        answers = dns.resolver.resolve(domain, 'MX', lifetime=timeout)
        return len(list(answers)) > 0
    except ImportError:
        pass
    except Exception:
        return False
    # Fallback: basic socket
    try:
        socket.setdefaulttimeout(timeout)
        socket.getaddrinfo(domain, 25)
        return True
    except Exception:
        return False


def is_valid_email_domain(email: str) -> tuple:
    """
    Returns (ok: bool, reason: str).
    Checks domain has MX before attempting send.
    """
    if not email or '@' not in email:
        return False, "Invalid email format"
    domain = email.split('@')[1].lower()
    if has_mx_record(domain):
        return True, "MX OK"
    return False, f"No MX record for {domain}"


# ==============================================================================
# HELPERS
# ==============================================================================

def is_company_name(name: str, company: str) -> bool:
    """Return True if recruiter_name looks like a company/generic name."""
    if not name:
        return True
    if name.lower() == company.lower():
        return True
    if " " not in name.strip():
        return True
    if name.lower() in {"hr", "recruiter", "hiring manager", "admin", "talent"}:
        return True
    return False


def load_sent_log() -> tuple:
    """Returns (sent_log list, sent_emails set)."""
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, encoding="utf-8") as f:
                log = json.load(f)
            return log, {e.get("email", "").lower() for e in log if e.get("email")}
        except Exception:
            pass
    return [], set()


def save_sent_log(log: list):
    os.makedirs(LOG_DIR, exist_ok=True)
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2, ensure_ascii=False)


# ==============================================================================
# SEND FUNCTION
# ==============================================================================

def send_email(to_email: str, recruiter_name: str, company: str, post: dict) -> tuple:
    """
    Send one email with a JD-tailored ATS resume attached.
    Returns (success: bool, error_msg: str).
    """
    company_ref = f"your post related to {company} " if company else ""
    body = EMAIL_BODY.format(
        recruiter_name=recruiter_name,
        company_ref=company_ref,
    )

    msg = MIMEMultipart()
    msg["From"]    = SMTP_USER
    msg["To"]      = to_email
    msg["Subject"] = EMAIL_SUBJECT
    msg.attach(MIMEText(body, "plain", "utf-8"))

    # ── Build JD-tailored resume ───────────────────────────────────────
    resume_path = None
    try:
        resume_path = resume_builder.generate(post)
        print(f"    Resume  : {os.path.basename(resume_path)} (tailored)")
    except Exception as e:
        # Fallback to base resume if builder fails
        print(f"    Resume  : [builder error: {e}] — using base resume")
        resume_path = RESUME_FILE

    if not resume_path or not os.path.exists(resume_path):
        return False, f"Resume file not found: {resume_path}"

    # ── Attach resume ──────────────────────────────────────────────────
    with open(resume_path, "rb") as f:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(f.read())
    encoders.encode_base64(part)
    part.add_header(
        "Content-Disposition",
        f'attachment; filename="{RESUME_NAME}"',
    )
    msg.attach(part)

    # ── Send ───────────────────────────────────────────────────────────
    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, timeout=30) as server:
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
        result = (True, "")
    except smtplib.SMTPRecipientsRefused as e:
        result = (False, f"SMTP rejected recipient: {e}")
    except Exception as e:
        result = (False, str(e))

    # ── Cleanup temp resume ────────────────────────────────────────────
    try:
        if resume_path and resume_path != RESUME_FILE and os.path.exists(resume_path):
            os.remove(resume_path)
    except Exception:
        pass

    return result


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    mode_label = "TEST (3 emails)" if TEST_MODE else "FULL BATCH"
    print("=" * 62)
    print(f"  SAP Email Sender — {mode_label}")
    print(f"  Date  : {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 62)

    if not os.path.exists(POSTS_FILE):
        print("  ERROR: linkedin_posts_today.json not found.")
        print("  Run brightdata_scrape.py + find_company_emails.py first.")
        return

    with open(POSTS_FILE, encoding="utf-8") as f:
        posts = json.load(f)

    sent_log, sent_emails = load_sent_log()
    print(f"  Posts loaded         : {len(posts)}")
    print(f"  Already sent         : {len(sent_emails)}")

    # Build queue — posts with email that haven't been sent yet
    queue = []
    seen_in_queue = set()
    for post in posts:
        email = (post.get("email") or "").strip().lower()
        if not post.get("has_email") or not email:
            continue
        if email in sent_emails or email in seen_in_queue:
            continue
        # Skip records explicitly marked invalid
        if post.get("email_valid") is False:
            continue
        seen_in_queue.add(email)
        queue.append(post)

    print(f"  Queue (new to send)  : {len(queue)}")

    if not queue:
        print("\n  Nothing to send — all emails already sent or no valid emails found.")
        print("  Run find_company_emails.py to find new email addresses.")
        return

    if TEST_MODE:
        print(f"\n  [TEST MODE] Sending first {TEST_LIMIT} emails only.")
        print(f"  Run with --all flag after confirming delivery.")
        queue = queue[:TEST_LIMIT]
    else:
        print(f"\n  [FULL MODE] Sending all {len(queue)} emails.")

    print()

    sent_count   = 0
    failed_count = 0
    skipped_mx   = 0
    results      = []

    for i, post in enumerate(queue):
        email   = post["email"].strip().lower()
        raw_name = post.get("recruiter_name") or ""
        company  = post.get("company") or ""

        recruiter_name = "Hiring Manager" if is_company_name(raw_name, company) else raw_name

        print(f"  [{i+1}/{len(queue)}] {email}")
        print(f"    To      : {recruiter_name} @ {company[:40]}")

        # ── DNS MX CHECK ───────────────────────────────────────────────
        ok, reason = is_valid_email_domain(email)
        if not ok:
            print(f"    SKIP    : {reason}")
            skipped_mx += 1
            results.append({"email": email, "company": company, "status": "skipped_no_mx", "reason": reason})
            continue

        print(f"    MX      : {reason}")

        # ── SEND ──────────────────────────────────────────────────────
        success, err = send_email(email, recruiter_name, company, post)

        if success:
            print(f"    STATUS  : SENT OK")
            sent_count += 1
            entry = {
                "recruiter_name": raw_name,
                "company":        company,
                "email":          email,
                "status":         "sent",
                "timestamp":      datetime.now().isoformat(),
            }
            sent_log.append(entry)
            sent_emails.add(email)
            save_sent_log(sent_log)
            results.append({**entry})
        else:
            print(f"    STATUS  : FAILED — {err}")
            failed_count += 1
            results.append({"email": email, "company": company, "status": "failed", "reason": err})

        # Polite delay between sends
        if i < len(queue) - 1:
            time.sleep(SEND_DELAY)

    # ── SUMMARY ──────────────────────────────────────────────────────
    print()
    print("=" * 62)
    print(f"  Sent successfully    : {sent_count}")
    print(f"  Failed               : {failed_count}")
    print(f"  Skipped (no MX)      : {skipped_mx}")
    print("=" * 62)

    if TEST_MODE and sent_count > 0:
        print()
        print("  [TEST MODE COMPLETE]")
        print("  Check your Gmail inbox — wait ~5 min for delivery reports.")
        print("  If all 3 arrived OK, run:")
        print("    python send_sap_emails.py --all")
        print("  to send the full batch.")

    if results:
        print()
        print("  This run:")
        for r in results:
            status = r.get("status", "?")
            icon   = "OK" if status == "sent" else ("MX" if "mx" in status else "!!")
            print(f"    [{icon}] {r['email']:40s} | {r.get('company','')[:25]}")


if __name__ == "__main__":
    main()
