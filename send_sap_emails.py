import json
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASS, BASE_DIR, LOG_DIR

POSTS_FILE = os.path.join(BASE_DIR, "linkedin_posts_today.json")
LOG_FILE   = os.path.join(LOG_DIR,  "email_sent_log.json")

EMAIL_TEMPLATE = """Dear {recruiter_name},

I came across your post on LinkedIn and wanted to reach out regarding SAP opportunities you may be hiring for.

I am Harsh Madan, a SAP S/4HANA Program Manager with 15+ years of end-to-end SAP implementation experience across ECC and S/4HANA environments. Key highlights:

• SAP S/4HANA Program Manager at Autodesk (May 2015–Present) — led full-cycle ECC to S/4HANA migrations
• Expert in Data Migration: LSMW, LTMC, SLT, SAP CPI — managed 10M+ record migrations with zero data loss
• Modules: FICO, MM, SD, MDG — cross-functional alignment across Finance, Procurement, and Sales
• Cutover Planning, SIT/UAT, Stakeholder Management — delivered on-time, zero critical post-go-live defects
• Tools: SAP Solution Manager, JIRA, Smartsheet, SAP MDG

Current CTC: 35 LPA | Expected: 40 LPA | Notice Period: Immediate
Open to: Remote / Hybrid roles

I would love to connect and discuss how my profile aligns with your current requirements. Please feel free to reach out or share any relevant JDs.

Kind regards,
Harsh Madan
+91 96679 64756
Madan.harsh1984@gmail.com
LinkedIn: https://sg.linkedin.com/in/harsh-madan-b818113b"""

def is_company_name(name, company):
    if not name:
        return True
    if name.lower() == company.lower():
        return True
    # If it's one word and doesn't look like a first name, it might be generic
    if " " not in name.strip():
        return True
    # Generic titles
    if name.lower() in ["hr", "recruiter", "hiring manager", "admin"]:
        return True
    return False

def send_email(to_email, recruiter_name, company):
    subject = "Application for SAP S/4HANA Program Manager / Data Migration Specialist Role"
    body = EMAIL_TEMPLATE.format(recruiter_name=recruiter_name)
    
    msg = MIMEMultipart()
    msg['From'] = SMTP_USER
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Failed to send to {to_email}: {e}")
        return False

def main():
    if not os.path.exists(POSTS_FILE):
        print("Posts file not found.")
        return

    with open(POSTS_FILE, 'r', encoding='utf-8') as f:
        posts = json.load(f)
        
    sent_log = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            sent_log = json.load(f)
            
    sent_emails = {entry['email'].lower() for entry in sent_log if 'email' in entry}
    
    new_emails_sent = []
    
    # Track emails processed in this run to avoid duplicates if same email is in multiple posts
    processed_in_run = set()

    for post in posts:
        email = post.get('email', '').strip().lower()
        if not post.get('has_email') or not email:
            continue
            
        if email in sent_emails or email in processed_in_run:
            continue
            
        raw_name = post.get('recruiter_name', '')
        company = post.get('company', '')
        
        if is_company_name(raw_name, company):
            recruiter_name = "Hiring Manager"
        else:
            recruiter_name = raw_name
            
        print(f"Sending to {email} ({recruiter_name} @ {company})...")
        if send_email(email, recruiter_name, company):
            log_entry = {
                "recruiter_name": raw_name,
                "company": company,
                "email": email,
                "status": "sent"
            }
            sent_log.append(log_entry)
            new_emails_sent.append(log_entry)
            processed_in_run.add(email)
            
            # Save log after each successful send
            with open(LOG_FILE, 'w', encoding='utf-8') as f:
                json.dump(sent_log, f, indent=2)
        else:
            print(f"Skipped {email} due to error.")

    print("\nSummary:")
    print(f"Total posts: {len(posts)}")
    print(f"Posts with email: {len([p for p in posts if p.get('has_email')])}")
    print(f"Already sent: {len(sent_emails)}")
    print(f"New emails sent: {len(new_emails_sent)}")
    for entry in new_emails_sent:
        print(f"- {entry['recruiter_name']} ({entry['company']}): {entry['email']}")

if __name__ == "__main__":
    main()
