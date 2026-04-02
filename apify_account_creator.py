"""
Apify Auto Account Creator — Harsh Madan Pipeline
===================================================
WHAT IT DOES:
  1. Uses GuerrillaMail public API (no browser, pure HTTP) to get a fresh
     throwaway email address instantly.
  2. Opens Apify signup page via Selenium and registers with that email.
  3. Polls GuerrillaMail inbox for Apify's verification email.
  4. Extracts the verification link and clicks it — account is now active.
  5. Saves the new API token to apify_accounts.json for use by apify_scrape.py

WHY GUERRILLAMAIL:
  - Free public JSON API, no signup, no CAPTCHA
  - Reads inbox via API — no browser needed for email
  - Unlimited throwaway addresses
  - Apify gives $5 free credits per new account (no card needed)

RUN THIS WHEN: apify_scrape.py reports "monthly limit exhausted"
"""

import urllib.request
import urllib.parse
import json
import re
import os
import sys
import time
from datetime import datetime

sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

from config import BASE_DIR, CHROMEDRIVER_PATH, CHROME_PROFILE_APIFY

# ── PATHS ────────────────────────────────────────────────────────────────────
OUTPUT_DIR      = BASE_DIR
ACCOUNTS_FILE   = os.path.join(OUTPUT_DIR, "apify_accounts.json")
CHROME_PROFILE  = CHROME_PROFILE_APIFY
CHROMEDRIVER    = CHROMEDRIVER_PATH

# ── GUERRILLAMAIL API ─────────────────────────────────────────────────────────
GM_API    = "http://api.guerrillamail.com/ajax.php"
GM_AGENT  = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
GM_IP     = "127.0.0.1"

# ── APIFY URLS ────────────────────────────────────────────────────────────────
APIFY_SIGNUP = "https://console.apify.com/sign-up"
APIFY_TOKEN  = "https://console.apify.com/settings/integrations"


# ═══════════════════════════════════════════════════════════════════════════════
# STEP A — GuerrillaMail: get temp email
# ═══════════════════════════════════════════════════════════════════════════════

class GuerrillaMail:
    def __init__(self):
        self.session_id = None
        self.email_addr = None
        self.cookies    = {}

    def _call(self, params: dict) -> dict:
        """Make a GET request to the GuerrillaMail API."""
        params["ip"]    = GM_IP
        params["agent"] = GM_AGENT
        query = urllib.parse.urlencode(params)
        url   = f"{GM_API}?{query}"

        req = urllib.request.Request(url)
        req.add_header("User-Agent", GM_AGENT)
        if self.session_id:
            req.add_header("Cookie", f"PHPSESSID={self.session_id}")

        with urllib.request.urlopen(req, timeout=15) as resp:
            # Extract new PHPSESSID from response headers
            set_cookie = resp.getheader("Set-Cookie", "")
            m = re.search(r"PHPSESSID=([^;]+)", set_cookie)
            if m:
                self.session_id = m.group(1)
            raw = resp.read().decode("utf-8")

        return json.loads(raw)

    def get_email(self) -> str:
        """Initialize session and get a random throwaway email address."""
        data = self._call({"f": "get_email_address", "lang": "en"})
        self.email_addr = data.get("email_addr", "")
        print(f"  [GuerrillaMail] Temp email: {self.email_addr}")
        return self.email_addr

    def set_custom_email(self, username: str) -> str:
        """Set a specific username part for the email (e.g. 'harshmadan2026')."""
        data = self._call({"f": "set_email_user", "email_user": username, "lang": "en"})
        self.email_addr = data.get("email_addr", "")
        print(f"  [GuerrillaMail] Custom email set: {self.email_addr}")
        return self.email_addr

    def wait_for_email(self, from_filter: str = "apify", max_wait: int = 180) -> str:
        """
        Poll inbox every 5 seconds until an email from 'from_filter' arrives.
        Returns the full email body text, or "" if timed out.
        """
        print(f"  [GuerrillaMail] Waiting for email from '{from_filter}' (max {max_wait}s)...")
        deadline = time.time() + max_wait
        seq = 0
        while time.time() < deadline:
            time.sleep(5)
            try:
                data  = self._call({"f": "check_email", "seq": seq})
                mails = data.get("list", [])
                for mail in mails:
                    sender  = str(mail.get("mail_from", "")).lower()
                    subject = str(mail.get("mail_subject", "")).lower()
                    mail_id = mail.get("mail_id", 0)
                    if from_filter.lower() in sender or from_filter.lower() in subject:
                        print(f"  [GuerrillaMail] Email found! Subject: {mail.get('mail_subject')}")
                        # Fetch full body
                        body_data = self._call({"f": "fetch_email", "email_id": mail_id})
                        return str(body_data.get("mail_body", ""))
                    # Advance sequence
                    if mail_id > seq:
                        seq = mail_id
            except Exception as e:
                print(f"  [GuerrillaMail] Poll error: {e}")
        print("  [GuerrillaMail] Timed out waiting for email.")
        return ""


# ═══════════════════════════════════════════════════════════════════════════════
# STEP B — Selenium: sign up on Apify
# ═══════════════════════════════════════════════════════════════════════════════

def get_driver():
    """Launch headless Chrome with a fresh temp profile."""
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service

    import shutil
    if os.path.exists(CHROME_PROFILE):
        shutil.rmtree(CHROME_PROFILE, ignore_errors=True)
    os.makedirs(CHROME_PROFILE, exist_ok=True)

    opts = Options()
    opts.add_argument(f"--user-data-dir={CHROME_PROFILE}")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-blink-features=AutomationControlled")
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option("useAutomationExtension", False)
    # Run visible (not headless) so CAPTCHA can be solved manually if needed
    # opts.add_argument("--headless=new")   # uncomment for fully headless

    svc = Service(CHROMEDRIVER)
    driver = webdriver.Chrome(service=svc, options=opts)
    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )
    return driver


def apify_signup(driver, email: str, password: str) -> bool:
    """
    Fill in and submit the Apify signup form.
    Returns True if signup succeeded, False otherwise.
    """
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    print(f"  [Apify] Opening signup page...")
    driver.get(APIFY_SIGNUP)
    time.sleep(4)

    try:
        wait = WebDriverWait(driver, 20)

        # Email field
        email_field = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "input[type='email'], input[name='email'], input[id='email']")
        ))
        email_field.clear()
        email_field.send_keys(email)
        time.sleep(0.5)

        # Click Next or find password field
        try:
            next_btn = driver.find_element(By.XPATH,
                "//button[contains(translate(.,'NEXT','next'),'next') or @type='submit'][1]")
            next_btn.click()
            time.sleep(2)
        except Exception:
            pass

        # Password field
        pwd_field = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "input[type='password']")
        ))
        pwd_field.clear()
        pwd_field.send_keys(password)
        time.sleep(0.5)

        # First name / Last name (if present)
        for fname_sel in ["input[name='firstName']", "input[placeholder*='first' i]", "input[id*='first' i]"]:
            try:
                f = driver.find_element(By.CSS_SELECTOR, fname_sel)
                if f.is_displayed():
                    f.clear(); f.send_keys("Harsh")
                    break
            except Exception: pass

        for lname_sel in ["input[name='lastName']", "input[placeholder*='last' i]", "input[id*='last' i]"]:
            try:
                l = driver.find_element(By.CSS_SELECTOR, lname_sel)
                if l.is_displayed():
                    l.clear(); l.send_keys("Madan")
                    break
            except Exception: pass

        # Submit signup
        submit = driver.find_element(By.CSS_SELECTOR,
            "button[type='submit'], button.signup-button, button[data-testid='signup-button']")
        submit.click()
        print("  [Apify] Signup form submitted.")
        time.sleep(5)

        # Check for success indicators
        current_url = driver.current_url
        page_text   = driver.find_element(By.TAG_NAME, "body").text.lower()
        if ("verify" in page_text or "check your email" in page_text
                or "confirm" in page_text or "console.apify.com" in current_url):
            print("  [Apify] Signup likely successful — check email for verification.")
            return True
        else:
            print(f"  [Apify] Signup status unclear. URL: {current_url}")
            print(f"  [Apify] Page snippet: {page_text[:300]}")
            return True  # proceed anyway, may still work

    except Exception as e:
        print(f"  [Apify] Signup error: {e}")
        return False


def apify_verify_email(driver, verify_link: str) -> bool:
    """Click the email verification link."""
    print(f"  [Apify] Clicking verify link: {verify_link[:80]}...")
    driver.get(verify_link)
    time.sleep(5)
    page = driver.find_element(By.TAG_NAME, "body").text.lower()
    if "verified" in page or "success" in page or "console.apify.com" in driver.current_url:
        print("  [Apify] Email verified successfully!")
        return True
    print(f"  [Apify] Verify page: {page[:200]}")
    return False


def apify_get_token(driver) -> str:
    """
    Navigate to Apify integrations/settings page and extract the API token.
    """
    print("  [Apify] Fetching API token...")
    driver.get(APIFY_TOKEN)
    time.sleep(5)

    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    wait = WebDriverWait(driver, 20)

    # Try to find token in input/code/span elements
    token = ""
    for sel in [
        "input[data-testid='api-token']",
        "input[id*='token' i]",
        "input[value^='apify_api_']",
        "code",
        "span[class*='token' i]",
        "div[class*='token' i]",
    ]:
        try:
            el = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, sel)))
            val = el.get_attribute("value") or el.text or ""
            val = val.strip()
            if val.startswith("apify_api_") or len(val) > 20:
                token = val
                break
        except Exception:
            continue

    if not token:
        # Try getting from page source
        src = driver.page_source
        m = re.search(r"apify_api_[A-Za-z0-9]{30,}", src)
        if m:
            token = m.group(0)

    if token:
        print(f"  [Apify] Token found: {token[:25]}...")
    else:
        print("  [Apify] Could not auto-extract token. Please copy it manually from:")
        print(f"  {APIFY_TOKEN}")

    return token


# ═══════════════════════════════════════════════════════════════════════════════
# STEP C — Save account to JSON
# ═══════════════════════════════════════════════════════════════════════════════

def save_account(email: str, password: str, token: str):
    accounts = []
    if os.path.exists(ACCOUNTS_FILE):
        try:
            with open(ACCOUNTS_FILE, "r") as f:
                accounts = json.load(f)
        except Exception:
            accounts = []

    accounts.append({
        "email":      email,
        "password":   password,
        "token":      token,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "status":     "active",
        "credits":    "$5 free",
    })

    with open(ACCOUNTS_FILE, "w") as f:
        json.dump(accounts, f, indent=2)

    print(f"\n  [Save] Account saved to {ACCOUNTS_FILE}")
    print(f"  [Save] Total accounts: {len(accounts)}")


def get_active_token() -> str:
    """
    Read apify_accounts.json and return the most recently created active token.
    Used by apify_scrape.py to always pick the freshest account.
    """
    if not os.path.exists(ACCOUNTS_FILE):
        return ""
    with open(ACCOUNTS_FILE, "r") as f:
        accounts = json.load(f)
    active = [a for a in accounts if a.get("status") == "active" and a.get("token")]
    if not active:
        return ""
    return active[-1]["token"]  # most recent


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    print("=" * 60)
    print("  Apify Auto Account Creator")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # ── A. Get temp email ────────────────────────────────────────────
    gm = GuerrillaMail()

    # Use a custom username so it looks more like a real email
    ts       = datetime.now().strftime("%m%d%H%M")
    username = f"harshmadan{ts}"
    email    = gm.set_custom_email(username)

    if not email or "@" not in email:
        # Fallback to random
        email = gm.get_email()

    # Password to use on Apify account
    password = f"Apify@{ts}#SAP"

    print(f"\n  Email    : {email}")
    print(f"  Password : {password}")
    print()

    # ── B. Selenium signup ────────────────────────────────────────────
    driver = get_driver()
    try:
        signup_ok = apify_signup(driver, email, password)
        if not signup_ok:
            print("  [ERROR] Signup failed. Exiting.")
            driver.quit()
            return

        # ── C. Wait for verification email ───────────────────────────
        body = gm.wait_for_email(from_filter="apify", max_wait=180)

        if not body:
            print("\n  [WARN] No verification email received.")
            print("  The account may still work — trying to get token anyway...")
        else:
            # Extract verification link
            links = re.findall(r'https?://[^\s"<>]+verify[^\s"<>]+', body)
            if not links:
                links = re.findall(r'https?://console\.apify\.com[^\s"<>]+', body)

            if links:
                verify_link = links[0].rstrip(".,)")
                apify_verify_email(driver, verify_link)
            else:
                print("  [WARN] Could not extract verification link from email body.")
                print(f"  Body snippet: {body[:400]}")

        # ── D. Get API token ─────────────────────────────────────────
        time.sleep(3)
        token = apify_get_token(driver)

        if not token:
            print("\n  [ACTION REQUIRED] Chrome is still open.")
            print("  Please manually:")
            print(f"  1. Go to: {APIFY_TOKEN}")
            print("  2. Copy your API token")
            print("  3. Paste it below and press Enter:")
            token = input("  Token: ").strip()

        # ── E. Save account ──────────────────────────────────────────
        save_account(email, password, token)

        print("\n" + "=" * 60)
        print("  SUCCESS! New Apify account ready.")
        print(f"  Token : {token[:30]}...")
        print(f"  Email : {email}")
        print("  This token is now saved and apify_scrape.py will use it.")
        print("=" * 60)

    finally:
        try:
            driver.quit()
        except Exception:
            pass


if __name__ == "__main__":
    main()
