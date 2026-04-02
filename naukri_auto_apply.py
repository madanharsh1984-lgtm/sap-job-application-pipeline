"""
Naukri Auto-Apply Automation — Harsh Madan
==========================================
Logs in to Naukri.com, searches 4 SAP titles in Remote + Delhi NCR,
15+ years experience, last 3 days, applies via Quick Apply or company site.
"""

import os, json, time, re, sys
from datetime import datetime
sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

from config import (
    RESUME_PATH, BASE_DIR, LOG_DIR,
    JOB_TITLES, NAUKRI_LOCATIONS as LOCATIONS, CANDIDATE,
    NAUKRI_EMAIL, NAUKRI_PASS,
    GOOGLE_EMAIL, GOOGLE_PASS,
    CHROME_BIN, CHROMEDRIVER_PATH, CHROME_PROFILE_NAUKRI,
)

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# ── CONFIG ────────────────────────────────────────────────────────
OUTPUT_FOLDER = BASE_DIR
LOG_FILE      = os.path.join(LOG_DIR, "naukri_applied_log.json")

# ── CHROME DRIVER ─────────────────────────────────────────────────
def get_driver():
    import shutil
    CHROMEDRIVER = CHROMEDRIVER_PATH
    TEMP_DIR     = CHROME_PROFILE_NAUKRI

    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR, ignore_errors=True)
    os.makedirs(TEMP_DIR, exist_ok=True)

    options = Options()
    options.binary_location = CHROME_BIN
    options.add_argument(f"--user-data-dir={TEMP_DIR}")
    options.add_argument("--profile-directory=Default")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-first-run")
    options.add_argument("--no-default-browser-check")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    service = Service(CHROMEDRIVER)
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(5)
    return driver


# ── NAUKRI LOGIN ──────────────────────────────────────────────────
def naukri_login(driver):
    print("  Navigating to Naukri login page...")
    driver.get("https://www.naukri.com/nlogin/login")
    time.sleep(4)

    if "naukri.com" in driver.current_url and "login" not in driver.current_url and "nlogin" not in driver.current_url:
        print("  Already logged in to Naukri.")
        return True

    # Try direct email+password login first
    try:
        email_field = WebDriverWait(driver, 8).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,
                "input[type='text'][placeholder*='Enter'], input[placeholder*='Email'], input[placeholder*='email'], #usernameField"))
        )
        email_field.clear()
        email_field.send_keys(NAUKRI_EMAIL)
        time.sleep(0.5)
        pass_field = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,
                "input[type='password'], #passwordField"))
        )
        pass_field.clear()
        pass_field.send_keys(NAUKRI_PASS)
        time.sleep(0.5)
        try:
            login_btn = driver.find_element(By.CSS_SELECTOR,
                "button[type='submit'], .loginButton, button.blue-btn, button[data-ga-track*='login']")
            login_btn.click()
        except Exception:
            pass_field.send_keys(Keys.RETURN)
        print("  Submitted Naukri email+password.")
        time.sleep(5)
        if "naukri.com" in driver.current_url and "login" not in driver.current_url and "nlogin" not in driver.current_url:
            print("  Naukri direct login successful.")
            return True
        print("  Direct login incomplete, trying Google OAuth...")
    except Exception as e:
        print(f"  Direct login attempt: {e} — trying Google OAuth...")

    # Try 'Continue with Google' OAuth
    try:
        google_btn = None
        for sel in [
            "//button[contains(.,'Google')]",
            "//a[contains(.,'Google')]",
            "//*[contains(@class,'google')][@role='button' or local-name()='button' or local-name()='a']",
            "//*[contains(@aria-label,'Google')]",
        ]:
            try:
                google_btn = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, sel))
                )
                print(f"  Found Google button: '{google_btn.text.strip()[:30]}'")
                break
            except Exception:
                pass

        if not google_btn:
            for css in ["[data-login-type='google']", ".google-login",
                        "[class*='googleLogin']", "button[title*='Google']"]:
                try:
                    google_btn = WebDriverWait(driver, 3).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, css))
                    )
                    break
                except Exception:
                    pass

        if not google_btn:
            print("  Google button not found — saving debug screenshot.")
            try:
                driver.save_screenshot(os.path.join(OUTPUT_FOLDER, "naukri_login_debug.png"))
            except Exception:
                pass
            return False

        try:
            google_btn.click()
        except Exception:
            driver.execute_script("arguments[0].click();", google_btn)
        print("  Clicked Google OAuth button.")
        time.sleep(4)

        original = driver.current_window_handle
        time.sleep(2)
        if len(driver.window_handles) > 1:
            for h in driver.window_handles:
                if h != original:
                    driver.switch_to.window(h)
                    print(f"  Google popup: {driver.current_url}")
                    break
            time.sleep(2)

        # Enter Google email if asked
        try:
            ei = WebDriverWait(driver, 6).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']"))
            )
            ei.clear()
            ei.send_keys(GOOGLE_EMAIL)
            ei.send_keys(Keys.RETURN)
            print("  Entered Google email.")
            time.sleep(3)
        except TimeoutException:
            pass

        # Enter Google password if asked
        try:
            pi = WebDriverWait(driver, 6).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']"))
            )
            pi.clear()
            pi.send_keys(GOOGLE_PASS)
            pi.send_keys(Keys.RETURN)
            print("  Entered Google password.")
            time.sleep(5)
        except TimeoutException:
            pass

        # Account picker
        for sel in [f"//div[contains(.,'{GOOGLE_EMAIL}')]",
                    f"//*[@data-email='{GOOGLE_EMAIL}']",
                    "//div[@role='listitem'][1]"]:
            try:
                WebDriverWait(driver, 4).until(
                    EC.element_to_be_clickable((By.XPATH, sel))
                ).click()
                time.sleep(3)
                break
            except Exception:
                pass

        # Allow/consent
        for sel in ["//button[contains(.,'Allow')]", "//button[contains(.,'Continue')]"]:
            try:
                WebDriverWait(driver, 4).until(
                    EC.element_to_be_clickable((By.XPATH, sel))
                ).click()
                time.sleep(3)
                break
            except Exception:
                pass

        if len(driver.window_handles) > 1:
            driver.switch_to.window(original)
            time.sleep(3)

    except Exception as e:
        print(f"  Google OAuth error: {e}")

    # Verify login
    for _ in range(15):
        cur = driver.current_url
        if "naukri.com" in cur and "login" not in cur and "nlogin" not in cur:
            print(f"  Logged in to Naukri. URL: {cur}")
            return True
        time.sleep(1)

    # OTP?
    if "otp" in driver.current_url.lower() or "verify" in driver.current_url.lower():
        print("  OTP required — waiting 45s for manual entry...")
        time.sleep(45)
        cur = driver.current_url
        if "naukri.com" in cur and "login" not in cur:
            return True

    print(f"  Login failed. URL: {driver.current_url}")
    try:
        driver.save_screenshot(os.path.join(OUTPUT_FOLDER, "naukri_login_result.png"))
    except Exception:
        pass
    return False


# ── LOG HELPERS ───────────────────────────────────────────────────
def load_log():
    if os.path.exists(LOG_FILE):
        try:
            return json.load(open(LOG_FILE, encoding="utf-8"))
        except Exception:
            return []
    return []

def save_log(log):
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2, ensure_ascii=False)

def already_applied(log, job_id):
    return any(str(e.get("job_id", "")) == str(job_id) for e in log)


# ── BUILD SEARCH URL ──────────────────────────────────────────────
def build_naukri_url(title, location, exp=15, days=3):
    title_slug = title.lower().replace(" ", "-")
    loc_slug   = location.lower().replace(" ", "-")
    base = "https://www.naukri.com/" + title_slug + "-jobs"
    if loc_slug and loc_slug != "remote":
        base += "-in-" + loc_slug
    params = f"?experience={exp}&jobAge={days}"
    if loc_slug == "remote":
        params += "&wfhType=1"
    return base + params


# ── APPLY TO JOB ──────────────────────────────────────────────────
def apply_to_job(driver, job_elem, log, title, location):
    try:
        # Get job ID
        job_id = job_elem.get_attribute("data-job-id") or job_elem.get_attribute("id") or ""
        if not job_id:
            try:
                link = job_elem.find_element(By.CSS_SELECTOR, "a[href*='/job-listings']")
                href = link.get_attribute("href") or ""
                m = re.search(r"-(\d+)\?", href)
                job_id = m.group(1) if m else href
            except Exception:
                job_id = str(time.time())

        if already_applied(log, job_id):
            return False

        # Get title/company
        job_title = ""
        company   = ""
        try:
            job_title = job_elem.find_element(By.CSS_SELECTOR, ".title, a.title, .jobTitle").text.strip()
        except Exception:
            pass
        try:
            company = job_elem.find_element(By.CSS_SELECTOR, ".comp-name, .companyInfo, .companyName").text.strip()
        except Exception:
            pass

        print(f"    Applying: {job_title} @ {company}")

        # Click Apply / Quick Apply
        applied = False
        for btn_sel in [
            ".apply-button button", "button.apply-button",
            "button[type='button'][class*='apply']",
            "//button[contains(.,'Apply')]",
            "//button[contains(.,'Quick Apply')]",
        ]:
            try:
                if btn_sel.startswith("//"):
                    btn = job_elem.find_element(By.XPATH, btn_sel)
                else:
                    btn = job_elem.find_element(By.CSS_SELECTOR, btn_sel)
                btn.click()
                print(f"      Clicked apply button.")
                applied = True
                time.sleep(3)
                break
            except Exception:
                pass

        if not applied:
            # Open job detail page and apply from there
            try:
                link = job_elem.find_element(By.CSS_SELECTOR, "a.title, a[href*='job-listings']")
                job_url = link.get_attribute("href")
                driver.execute_script("window.open(arguments[0]);", job_url)
                time.sleep(2)
                driver.switch_to.window(driver.window_handles[-1])
                time.sleep(2)
                for btn_sel in ["button.apply-button", "//button[contains(.,'Apply')]"]:
                    try:
                        if btn_sel.startswith("//"):
                            btn = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, btn_sel)))
                        else:
                            btn = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, btn_sel)))
                        btn.click()
                        applied = True
                        time.sleep(3)
                        break
                    except Exception:
                        pass
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
            except Exception as e:
                print(f"      Detail page apply error: {e}")

        if applied:
            # Handle apply modal / confirmation
            try:
                # Fill phone if asked
                phone_field = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='tel'], input[placeholder*='phone'], input[placeholder*='Phone']"))
                )
                phone_field.clear()
                phone_field.send_keys(CANDIDATE["phone"])
            except Exception:
                pass

            # Submit
            for sub_sel in ["//button[contains(.,'Apply')]", "//button[contains(.,'Submit')]",
                            "//button[contains(.,'Confirm')]"]:
                try:
                    WebDriverWait(driver, 3).until(
                        EC.element_to_be_clickable((By.XPATH, sub_sel))
                    ).click()
                    time.sleep(2)
                    break
                except Exception:
                    pass

            # Dismiss modal
            for dismiss in ["//button[contains(.,'Close')]", "//button[@aria-label='Close']",
                            "//span[@class='crossIcon']"]:
                try:
                    WebDriverWait(driver, 2).until(
                        EC.element_to_be_clickable((By.XPATH, dismiss))
                    ).click()
                    break
                except Exception:
                    pass

            log.append({
                "job_id":     str(job_id),
                "job_title":  job_title,
                "company":    company,
                "search_title": title,
                "location":   location,
                "applied_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "status":     "Applied"
            })
            save_log(log)
            print(f"      APPLIED: {job_title} @ {company}")
            return True

    except Exception as e:
        print(f"    Apply error: {e}")
    return False


# ── SEARCH AND APPLY ──────────────────────────────────────────────
def search_and_apply(driver, title, location, log):
    applied = 0
    url = build_naukri_url(title, location)
    print(f"  Searching '{title}' in {location}...")
    print(f"  URL: {url}")

    try:
        driver.get(url)
        time.sleep(4)

        # Scroll to load more
        for _ in range(3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

        # Get job cards
        cards = driver.find_elements(By.CSS_SELECTOR,
            ".srp-jobtuple-wrapper, article.jobTuple, .jobTupleHeader, .job-card")
        print(f"    Found {len(cards)} job cards.")

        for i, card in enumerate(cards[:15]):
            try:
                print(f"    Card {i+1}/{min(len(cards),15)}...")
                result = apply_to_job(driver, card, log, title, location)
                if result:
                    applied += 1
                time.sleep(1)
            except Exception as e:
                print(f"    Card error: {e}")
                continue

    except Exception as e:
        print(f"  Search error for '{title}' in {location}: {e}")

    return applied


# ── MAIN ──────────────────────────────────────────────────────────
def main():
    print("=" * 55)
    print(f"  Naukri Auto-Apply — Harsh Madan")
    print(f"  {datetime.now().strftime('%d %b %Y %H:%M')}")
    print("=" * 55)

    log = load_log()
    print(f"  Previously applied: {len(log)} jobs")
    print()

    os.system("taskkill /f /im chrome.exe /t 2>nul")
    os.system("taskkill /f /im chromedriver.exe /t 2>nul")
    time.sleep(4)

    driver = None
    try:
        driver = get_driver()
        print("  Chrome launched.")

        if not naukri_login(driver):
            print("ERROR: Could not log in to Naukri. Exiting.")
            return

        total_applied = 0
        summary = {}

        for title in JOB_TITLES:
            summary[title] = {}
            for location in LOCATIONS:
                count = search_and_apply(driver, title, location, log)
                summary[title][location] = count
                total_applied += count
                print(f"  [{title} / {location}] Applied: {count}")
                time.sleep(2)

        print()
        print("=" * 55)
        print(f"  DONE. Total applied: {total_applied}")
        for t, locs in summary.items():
            for loc, cnt in locs.items():
                print(f"    {t} / {loc}: {cnt}")
        print("=" * 55)

        with open(os.path.join(OUTPUT_FOLDER, "naukri_summary.json"), "w", encoding="utf-8") as f:
            json.dump({
                "date":          datetime.now().strftime("%Y-%m-%d"),
                "total_applied": total_applied,
                "breakdown":     summary
            }, f, indent=2)

    except Exception as e:
        print(f"FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if driver:
            try:
                driver.quit()
            except Exception:
                pass

if __name__ == "__main__":
    main()
