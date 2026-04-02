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

# ── GOOGLE ACCOUNT (for OAuth login flows in Selenium) ────────────────────────
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

# ── CHROME / SELENIUM ─────────────────────────────────────────────────────────
CHROME_BIN        = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
CHROMEDRIVER_PATH = r"C:\Users\YOUR_USERNAME\.wdm\drivers\chromedriver\win64\VERSION\chromedriver-win32\chromedriver.exe"  # ← FILL THIS

CHROME_PROFILE_LI     = r"C:\Users\YOUR_USERNAME\AppData\Local\Temp\selenium_li_fresh"     # ← FILL THIS
CHROME_PROFILE_NAUKRI = r"C:\Users\YOUR_USERNAME\AppData\Local\Temp\selenium_naukri_fresh"  # ← FILL THIS
CHROME_PROFILE_APIFY  = r"C:\Users\YOUR_USERNAME\AppData\Local\Temp\selenium_apify_fresh"   # ← FILL THIS

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
