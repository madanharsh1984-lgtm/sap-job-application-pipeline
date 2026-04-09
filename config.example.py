# =============================================================================
# config.example.py — SAP Job Application Pipeline — CONFIGURATION TEMPLATE
# =============================================================================
# INSTRUCTIONS FOR NEW AGENT / NEW MACHINE:
#   1. Copy this file:   cp config.example.py config.py
#   2. Fill in all values marked with  ← FILL THIS
#   3. Never commit config.py to GitHub (it is in .gitignore)
# =============================================================================

import os

# ── PATHS ─────────────────────────────────────────────────────────────────────
# Root folder where all scripts and data files live
BASE_DIR    = r"C:\Users\YOUR_USERNAME\OneDrive\Desktop\Linkdin Job Application"   # ← FILL THIS
RESUME_PATH = os.path.join(BASE_DIR, "Harsh_Madan_SAP_PM_AgileES.docx")
LOG_DIR     = BASE_DIR

# ── CANDIDATE PROFILE ─────────────────────────────────────────────────────────
CANDIDATE = {
    "name":         "Your Full Name",            # ← FILL THIS
    "email":        "your.email@gmail.com",       # ← FILL THIS
    "phone":        "9999999999",                 # ← FILL THIS (digits only)
    "headline":     "SAP S/4HANA Program Manager | Data Migration Specialist",
    "years_exp":    "15",
    "current_ctc":  "35",                         # in LPA
    "expected_ctc": "40",                         # in LPA
    "notice":       "Immediate",
    "city":         "Delhi",
    "linkedin":     "https://linkedin.com/in/your-profile",   # ← FILL THIS
    "visa":         "Yes",
    "relocation":   "No",
    "work_auth":    "India",
}

# ── GMAIL / SMTP ──────────────────────────────────────────────────────────────
# Use a Gmail App Password (NOT your regular Gmail password)
# How to create: Google Account → Security → 2-Step Verification → App Passwords
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT   = 465
SMTP_USER   = "your.email@gmail.com"     # ← FILL THIS
SMTP_PASS   = "xxxx xxxx xxxx xxxx"      # ← FILL THIS (Gmail App Password, 16 chars)

# ── GOOGLE ACCOUNT (optional OAuth fallback) ───────────────────────────────────
GOOGLE_EMAIL = "your.email@gmail.com"    # ← FILL THIS
GOOGLE_PASS  = "YourGooglePassword"      # ← FILL THIS

# ── LINKEDIN DIRECT LOGIN ─────────────────────────────────────────────────────
LINKEDIN_EMAIL = "your.email@gmail.com"  # ← FILL THIS
LINKEDIN_PASS  = "YourLinkedInPassword"  # ← FILL THIS

# ── NAUKRI DIRECT LOGIN ───────────────────────────────────────────────────────
NAUKRI_EMAIL = "your.email@gmail.com"    # ← FILL THIS
NAUKRI_PASS  = "YourNaukriPassword"      # ← FILL THIS

# ── BRIGHT DATA ───────────────────────────────────────────────────────────────
# Get from: https://brightdata.com → Account Settings → API Keys
# Trial accounts get $5 free; paid plans from $0.001/record
BRIGHTDATA_API_KEY = ""    # ← FILL THIS (e.g. "ed991925-xxxx-xxxx-xxxx-xxxxxxxxxxxx")

# ── APIFY ─────────────────────────────────────────────────────────────────────
# Get from: https://console.apify.com/settings/integrations
# Leave blank to use apify_accounts.json token rotation instead
APIFY_TOKEN = ""    # ← FILL THIS (e.g. "apify_api_xxxxxxxx...")

# ── PLAYWRIGHT APPLY ENGINE ────────────────────────────────────────────────────
# Keep empty to use defaults from apply_engine_playwright.py
PLAYWRIGHT_HEADLESS = True
PLAYWRIGHT_WORKERS = 5
PLAYWRIGHT_MAX_RETRIES = 2
PLAYWRIGHT_USE_API_APPLY = True
PLAYWRIGHT_SESSION_DIR = os.path.join(BASE_DIR, ".playwright_sessions")
PLAYWRIGHT_REDIS_URL = ""               # optional (e.g. redis://localhost:6379/0)
PLAYWRIGHT_PROXY_LIST = ""              # optional comma-separated proxies

# Optional captcha solver integration
CAPTCHA_PROVIDER = ""                   # "2captcha" or "capmonster"
CAPTCHA_API_KEY = ""                    # provider API key

# ── JOB SEARCH CONFIG ─────────────────────────────────────────────────────────
JOB_TITLES = [
    "SAP S4 HANA Project Manager",
    "SAP Project Manager",
    "SAP SD MM Consultant",
    "SAP Data Migration Consultant",
]

NAUKRI_LOCATIONS = ["Remote", "Delhi NCR"]

# ── EMAIL SIGNATURE ───────────────────────────────────────────────────────────
EMAIL_SIGNATURE = """
Kind regards,
Your Name
Your Phone
Your Email
LinkedIn: https://linkedin.com/in/your-profile
"""
