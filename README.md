# SAP Job Application Pipeline

Fully automated daily job application pipeline for SAP professionals — scrapes LinkedIn & Naukri for fresh openings, extracts recruiter emails, sends tailored applications, and auto-applies via Easy Apply on LinkedIn and Naukri.

---

## What It Does (Daily at 9:00 AM IST)

```
Step 1 → Scrape LinkedIn recruiter posts (Apify) + job listings (JobSpy)
Step 2 → Extract emails from posts → send tailored Gmail applications
Step 3 → LinkedIn Easy Apply (Selenium) — 4 SAP titles, Remote, last 24h
Step 4 → Naukri Auto-Apply (Selenium) — Remote + Delhi NCR, last 3 days
```

---

## Project Structure

```
├── config.py              ← PRIVATE — your secrets (git-ignored, never commit)
├── config.example.py      ← Safe template — copy → config.py and fill in values
│
├── apify_scrape.py        ← Step 1a: Scrape LinkedIn recruiter posts via Apify
├── apify_account_creator.py ← Creates fresh Apify accounts when credits run out
├── jobspy_scrape.py       ← Step 1b: Scrape job listings via JobSpy (free)
│
├── send_sap_emails.py     ← Step 2: Send Gmail applications to email leads
│
├── linkedin_easy_apply.py ← Step 3: Selenium Easy Apply on LinkedIn
├── naukri_auto_apply.py   ← Step 4: Selenium auto-apply on Naukri
│
├── Create_SAP_Job_Drafts.py    ← Utility: create Outlook drafts with resume
├── Run_Full_Pipeline.bat       ← Run all steps manually (double-click)
├── Run_LinkedIn_Easy_Apply.bat ← Run LinkedIn Easy Apply manually
├── Run_Naukri_Apply.bat        ← Run Naukri apply manually
├── Create_Apify_Account.bat    ← Create new Apify account (when credits gone)
├── Install_JobSpy.bat          ← Install required Python packages
│
└── README.md
```

---

## Setup (New Machine / New Agent)

### 1. Prerequisites
- Python 3.10+ → [python.org](https://python.org)
- Google Chrome → [chrome.google.com](https://chrome.google.com)
- Git → [git-scm.com](https://git-scm.com)

### 2. Install dependencies
```bash
pip install python-jobspy selenium webdriver-manager python-docx requests
```
Or double-click **`Install_JobSpy.bat`**.

### 3. Configure secrets
```bash
copy config.example.py config.py
```
Open `config.py` and fill in all values marked `← FILL THIS`:
- Gmail App Password (not your regular password — create at [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords))
- LinkedIn login credentials
- Naukri login credentials
- Apify API token (from [console.apify.com/settings/integrations](https://console.apify.com/settings/integrations))
- Your `BASE_DIR` (full path to this project folder)
- ChromeDriver path (auto-managed by `webdriver-manager`, or set manually)

### 4. Run manually
```bash
python apify_scrape.py       # Scrape LinkedIn posts → linkedin_posts_today.json
python send_sap_emails.py    # Send emails to extracted leads
python linkedin_easy_apply.py
python naukri_auto_apply.py
```
Or double-click **`Run_Full_Pipeline.bat`**.

### 5. Schedule daily automation (Windows Task Scheduler)
The pipeline is pre-configured to run at **9:00 AM IST** via Windows Task Scheduler.
Check Task Scheduler → `SAP_LinkedIn_EasyApply` and `SAP_Naukri_AutoApply`.

---

## Scraping Tools

| Tool | Type | Cost | Used For |
|---|---|---|---|
| **Apify** `harvestapi/linkedin-post-search` | API | $29/month (Starter) | LinkedIn recruiter posts with emails |
| **JobSpy** | Free library | $0 | LinkedIn + Indeed job listings |

- **Apify** gives 50–80 recruiter email leads/day — highest value
- **JobSpy** is the free fallback — fewer email leads but zero cost
- When Apify credits run out → double-click `Create_Apify_Account.bat` or upgrade to Apify Starter ($29/month)

---

## Security

- **`config.py`** — never committed. Contains all passwords and API tokens.
- **`apify_accounts.json`** — never committed. Contains Apify account tokens.
- **`email_sent_log.json`** — never committed. Contains recruiter emails.
- **Resume `.docx` files** — never committed. Share separately.
- **`.gitignore`** enforces all of the above automatically.

---

## Candidate Profile

- **Name:** Harsh Madan
- **Title:** SAP S/4HANA Program Manager | Data Migration Specialist
- **Experience:** 15+ years (ECC → S/4HANA)
- **Modules:** FICO, MM, SD, MDG, LSMW, LTMC, SLT, SAP CPI
- **Current:** Autodesk (May 2015–Present)
- **CTC:** 35 LPA → Expected 40 LPA | Notice: Immediate
- **Open to:** Remote / Hybrid

---

## Stats
- Total emails sent to date: **89+**
- Daily run: 9:00 AM IST (automated)
- Platforms: LinkedIn, Naukri, Indeed (via JobSpy)
