"""
Indeed.com Auto-Apply Automation — Harsh Madan
===============================================
- Logs in via Google Sign-In (madan.harsh1984@gmail.com)
- Searches 4 SAP job titles on Indeed India
- Filters: Remote, Last 24h, Relevant experience
- Applies via Indeed Easy Apply
- Logs all applications to indeed_applied_log.json
- Saves summary to indeed_summary.json

Uses main Chrome profile (Google already signed in — no password needed).
Chrome must be closed before running (taskkill runs automatically).
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
import time, json, os, re
from datetime import datetime

# ─── CONFIG ────────────────────────────────────────────────────
INDEED_EMAIL  = "madan.harsh1984@gmail.com"
OUTPUT_FOLDER = r"C:\Users\madan\OneDrive\Desktop\Linkdin Job Application"
LOG_FILE      = os.path.join(OUTPUT_FOLDER, "indeed_applied_log.json")
SUMMARY_FILE  = os.path.join(OUTPUT_FOLDER, "indeed_summary.json")
RESUME_PATH   = os.path.join(OUTPUT_FOLDER, "Harsh_Madan_SAP_PM_AgileES.docx")

JOB_TITLES = [
    "SAP S4 HANA Project Manager",
    "SAP Project Manager",
    "SAP SD MM Consultant",
    "SAP Data Migration Consultant",
]

# Indeed Easy Apply form answers
ANSWERS = {
    "years":        "15",
    "experience":   "15",
    "notice":       "0",
    "immediately":  "Yes",
    "salary":       "40",
    "expected":     "40",
    "current":      "35",
    "ctc":          "40",
    "city":         "Delhi",
    "location":     "Delhi",
    "phone":        "9667964756",
    "mobile":       "9667964756",
    "sponsor":      "Yes",
    "visa":         "Yes",
    "authorize":    "No",
    "relocate":     "No",
    "remote":       "Yes",
    "available":    "Immediately",
    "name":         "Harsh Madan",
    "first":        "Harsh",
    "last":         "Madan",
    "email":        INDEED_EMAIL,
    "linkedin":     "https://sg.linkedin.com/in/harsh-madan-b818113b",
    "website":      "https://sg.linkedin.com/in/harsh-madan-b818113b",
}

# ─── DRIVER ────────────────────────────────────────────────────
def get_driver():
    """
    Launch Chrome with main user profile — Google + Indeed session active.
    Chrome must be closed before calling (taskkill in main()).
    """
    CHROMEDRIVER = r"C:\Users\madan\.wdm\drivers\chromedriver\win64\146.0.7680.165\chromedriver-win32\chromedriver.exe"
    CHROME_BIN   = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

    options = Options()
    options.binary_location = CHROME_BIN
    options.add_argument(r"--user-data-dir=C:\Users\madan\AppData\Local\Google\Chrome\User Data")
    options.add_argument("--profile-directory=Default")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    service = Service(CHROMEDRIVER)
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(6)
    return driver

# ─── HELPERS ───────────────────────────────────────────────────
def fill_field(el, value):
    try:
        el.click()
        el.send_keys(Keys.CONTROL + "a")
        el.send_keys(Keys.DELETE)
        el.send_keys(str(value))
        time.sleep(0.3)
    except Exception:
        pass

def safe_click(driver, el):
    try:
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
        time.sleep(0.3)
        el.click()
    except Exception:
        try:
            driver.execute_script("arguments[0].click();", el)
        except Exception:
            pass

def close_popups(driver):
    """Dismiss any cookie/notification/modal overlays."""
    for sel in [
        "button[id*='close']", "button[aria-label*='close' i]",
        "button[aria-label*='dismiss' i]", "[data-testid='dismiss-button']",
        ".icl-CloseButton", "button.css-1vg6q84",
    ]:
        try:
            btns = driver.find_elements(By.CSS_SELECTOR, sel)
            for btn in btns:
                if btn.is_displayed():
                    btn.click()
                    time.sleep(0.5)
        except Exception:
            pass

def load_log():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_log(log):
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2, ensure_ascii=False)

def already_applied(log, job_id):
    return any(e.get("job_id") == job_id for e in log)

def extract_job_id(url):
    m = re.search(r"jk=([a-z0-9]+)", url)
    return m.group(1) if m else url[-16:]

# ─── INDEED GOOGLE LOGIN ────────────────────────────────────────
def indeed_google_login(driver):
    """
    Log in to Indeed using 'Continue with Google'.
    Since Chrome is launched with the main profile, Google is already
    signed in — OAuth completes automatically with account selection only.
    """
    print("  Checking Indeed login status...")
    driver.get("https://in.indeed.com/")
    time.sleep(4)

    # Already logged in if profile avatar / "HM" visible
    try:
        driver.find_element(By.CSS_SELECTOR, "[data-testid='UserDropdown'], .css-1ioi40n, [aria-label*='Account']")
        print("  Already logged in to Indeed.")
        return True
    except NoSuchElementException:
        pass

    if "profile" in driver.current_url.lower() or "dashboard" in driver.current_url.lower():
        print("  Already logged in (URL check).")
        return True

    print("  Not logged in — attempting Google Sign-In...")

    try:
        # Navigate to Indeed sign-in
        driver.get("https://secure.indeed.com/auth?hl=en_IN&co=IN")
        time.sleep(3)

        # ── Find 'Continue with Google' button ──────────────────
        google_btn = None
        google_xpaths = [
            "//a[contains(.,'Google') and contains(@href,'google')]",
            "//button[contains(.,'Google')]",
            "//*[@data-tn-element='google-auth-button']",
            "//a[contains(@class,'google')]",
            "//*[contains(@aria-label,'Google')]",
            "//div[@role='button' and contains(.,'Google')]",
            "//span[contains(.,'Continue with Google')]/..",
        ]
        for xp in google_xpaths:
            try:
                google_btn = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, xp))
                )
                print(f"  Found Google button: '{google_btn.text.strip()[:40]}'")
                break
            except TimeoutException:
                pass

        # CSS fallback
        if not google_btn:
            for css in ["[data-tn-element='google-auth-button']",
                        ".css-ql2tfq[href*='google']",
                        "a[href*='accounts.google.com']",
                        "[class*='GoogleButton']"]:
                try:
                    google_btn = WebDriverWait(driver, 3).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, css))
                    )
                    break
                except TimeoutException:
                    pass

        if not google_btn:
            print("  Google button not found — saving screenshot.")
            try:
                driver.save_screenshot(os.path.join(OUTPUT_FOLDER, "indeed_login_debug.png"))
            except Exception:
                pass
            # Wait for manual login
            print("  Waiting 45s for manual login...")
            time.sleep(45)
            return True

        safe_click(driver, google_btn)
        print("  Clicked 'Continue with Google'.")
        time.sleep(4)

        # ── Handle Google account picker popup ──────────────────
        original_window = driver.current_window_handle
        if len(driver.window_handles) > 1:
            for handle in driver.window_handles:
                if handle != original_window:
                    driver.switch_to.window(handle)
                    print(f"  Switched to Google popup: {driver.current_url}")
                    break
            time.sleep(3)

        # Select correct Google account
        for sel in [
            f"//div[contains(.,'{INDEED_EMAIL}')]",
            f"//li[contains(.,'{INDEED_EMAIL}')]",
            f"//*[@data-email='{INDEED_EMAIL}']",
            f"//div[@role='option' and contains(.,'{INDEED_EMAIL}')]",
            "//div[@role='listitem'][1]",
            "//li[@role='presentation'][1]",
        ]:
            try:
                acct = WebDriverWait(driver, 6).until(
                    EC.element_to_be_clickable((By.XPATH, sel))
                )
                print(f"  Selecting account: {INDEED_EMAIL}")
                acct.click()
                time.sleep(4)
                break
            except TimeoutException:
                pass

        # Handle consent screen
        for xp in ["//button[contains(.,'Allow')]", "//button[contains(.,'Continue')]",
                   "//button[contains(.,'Confirm')]"]:
            try:
                btn = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, xp))
                )
                btn.click()
                print("  Clicked Allow/Continue on consent screen.")
                time.sleep(4)
                break
            except TimeoutException:
                pass

        # Switch back to main window
        if len(driver.window_handles) > 1:
            driver.switch_to.window(original_window)
            time.sleep(3)

        # Verify login
        for _ in range(15):
            cur = driver.current_url
            if "indeed.com" in cur and "auth" not in cur and "login" not in cur:
                print(f"  Logged in to Indeed. URL: {cur}")
                return True
            time.sleep(1)

        print(f"  Login result URL: {driver.current_url}")
        try:
            driver.save_screenshot(os.path.join(OUTPUT_FOLDER, "indeed_login_result.png"))
        except Exception:
            pass
        return True  # Proceed anyway

    except Exception as e:
        print(f"  Indeed Google login error: {e}")
        try:
            driver.save_screenshot(os.path.join(OUTPUT_FOLDER, "indeed_login_error.png"))
        except Exception:
            pass
        return False

# ─── EASY APPLY FORM HANDLER ────────────────────────────────────
def handle_easy_apply(driver, job_id, job_title, company):
    """
    Step through Indeed Easy Apply multi-page form.
    Returns: 'submitted' | 'incomplete' | 'error'
    """
    for step in range(12):
        time.sleep(2)

        # Check success
        for success_sel in [
            "//h1[contains(.,'application was sent')]",
            "//h2[contains(.,'application was sent')]",
            "//h1[contains(.,'Applied')]",
            "//*[contains(@data-testid,'post-apply')]",
            "//*[contains(.,'application has been submitted')]",
        ]:
            try:
                driver.find_element(By.XPATH, success_sel)
                print(f"    SUCCESS at step {step+1}")
                return "submitted"
            except NoSuchElementException:
                pass

        close_popups(driver)

        # Upload resume if file input present
        for inp in driver.find_elements(By.CSS_SELECTOR, "input[type='file']"):
            try:
                driver.execute_script("arguments[0].style.display='block';", inp)
                inp.send_keys(RESUME_PATH)
                time.sleep(1.5)
                print(f"    Uploaded resume at step {step+1}")
            except Exception:
                pass

        # Fill text/select/textarea fields
        field_containers = driver.find_elements(
            By.CSS_SELECTOR,
            ".ia-Questions-item, .css-k5flys, [data-testid='FormField'], "
            ".ia-BasePage-content div[class*='Field'], fieldset"
        )
        for container in field_containers:
            try:
                try:
                    label = container.find_element(By.CSS_SELECTOR, "label, legend, h3").text.lower()
                except Exception:
                    label = container.text.lower()[:80]

                # Radio buttons (Yes/No questions)
                radios = container.find_elements(By.CSS_SELECTOR, "input[type='radio']")
                if radios:
                    matched = False
                    for kw, ans in ANSWERS.items():
                        if kw in label:
                            for radio in radios:
                                radio_label = ""
                                try:
                                    radio_label = driver.find_element(
                                        By.CSS_SELECTOR, f"label[for='{radio.get_attribute('id')}']"
                                    ).text.lower()
                                except Exception:
                                    pass
                                if ans.lower() in radio_label:
                                    safe_click(driver, radio)
                                    matched = True
                                    break
                            if matched:
                                break
                    continue

                # Select dropdowns
                selects = container.find_elements(By.TAG_NAME, "select")
                for sel_el in selects:
                    sel_obj = Select(sel_el)
                    for kw, ans in ANSWERS.items():
                        if kw in label:
                            for opt in sel_obj.options:
                                if ans.lower() in opt.text.lower():
                                    sel_obj.select_by_visible_text(opt.text)
                                    break
                            else:
                                if len(sel_obj.options) > 1:
                                    sel_obj.select_by_index(1)
                            break

                # Text inputs
                inputs = container.find_elements(
                    By.CSS_SELECTOR,
                    "input:not([type=hidden]):not([type=file]):not([type=radio]):not([type=checkbox])"
                )
                for inp in inputs:
                    existing = (inp.get_attribute("value") or "").strip()
                    if existing:
                        continue
                    for kw, ans in ANSWERS.items():
                        if kw in label:
                            fill_field(inp, ans)
                            break

                # Textareas
                textareas = container.find_elements(By.TAG_NAME, "textarea")
                for ta in textareas:
                    existing = (ta.get_attribute("value") or "").strip()
                    if not existing:
                        fill_field(ta, (
                            "SAP S/4HANA Program Manager with 15+ years experience. "
                            "Led 12 global go-lives. Immediate joiner. Remote."
                        ))

            except StaleElementReferenceException:
                pass
            except Exception:
                pass

        # Click Continue / Next / Submit in priority order
        clicked = False
        for btn_text in ["Submit your application", "Submit application", "Submit",
                         "Continue", "Next", "Review your application", "Review"]:
            for by_method, selector in [
                (By.XPATH, f"//button[normalize-space()='{btn_text}']"),
                (By.XPATH, f"//button[contains(.,'{btn_text}')]"),
                (By.CSS_SELECTOR, f"button[data-testid*='submit']"),
                (By.CSS_SELECTOR, f"button[data-testid*='continue']"),
                (By.CSS_SELECTOR, f"button[data-testid*='next']"),
            ]:
                try:
                    btn = WebDriverWait(driver, 3).until(
                        EC.element_to_be_clickable((by_method, selector))
                    )
                    safe_click(driver, btn)
                    clicked = True
                    time.sleep(2)
                    break
                except TimeoutException:
                    pass
            if clicked:
                break

        if not clicked:
            # Check if modal/overlay gone = success
            try:
                driver.find_element(By.CSS_SELECTOR,
                    ".ia-BasePage, [data-testid='ia-BasePage'], .jobsearch-EasyApplyModal")
            except NoSuchElementException:
                return "submitted"
            return "incomplete"

        # Re-check success after each click
        for success_sel in [
            "//h1[contains(.,'application was sent')]",
            "//h2[contains(.,'application was sent')]",
            "//*[contains(@data-testid,'post-apply')]",
        ]:
            try:
                driver.find_element(By.XPATH, success_sel)
                return "submitted"
            except NoSuchElementException:
                pass

    return "max_steps_reached"

# ─── SEARCH & APPLY ────────────────────────────────────────────
def search_and_apply(driver, title, log):
    """Search Indeed for a job title and apply to all Easy Apply jobs."""
    applied_count = 0
    encoded_title = title.replace(" ", "+")

    # Build search URL: India, Remote, Last 24h, Easy Apply
    url = (
        f"https://in.indeed.com/jobs?q={encoded_title}"
        f"&l=India&sc=0kf%3Aattr(DSQF7)%3B&fromage=1&sort=date"
        f"&remotejob=032b3046-06a3-4876-8dfd-474eb5e7ed11"
    )

    print(f"\n  Searching: {title}")
    driver.get(url)
    time.sleep(4)
    close_popups(driver)

    # Collect job cards
    job_cards = driver.find_elements(
        By.CSS_SELECTOR,
        ".job_seen_beacon, .tapItem, [data-testid='jobCard'], .resultContent"
    )
    print(f"  Found {len(job_cards)} job cards")

    for i, card in enumerate(job_cards[:25]):
        try:
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", card)
            time.sleep(0.5)
            safe_click(driver, card)
            time.sleep(2.5)
            close_popups(driver)

            # Get job details from right panel
            cur_url = driver.current_url
            job_id  = extract_job_id(cur_url)

            if already_applied(log, job_id):
                print(f"    [{i+1}] Skip (already applied): {job_id}")
                continue

            try:
                job_title_el = driver.find_element(
                    By.CSS_SELECTOR,
                    ".jobsearch-JobInfoHeader-title, h1[data-testid='jobTitle'], .icl-u-xs-mb--xs"
                )
                act_title = job_title_el.text.strip()
            except Exception:
                act_title = title

            try:
                company_el = driver.find_element(
                    By.CSS_SELECTOR,
                    "[data-testid='inlineHeader-companyName'], .css-1ioi40n, .icl-u-lg-mr--sm"
                )
                company = company_el.text.strip()
            except Exception:
                company = "Unknown"

            # Look for Indeed Easy Apply button
            easy_apply_btn = None
            for sel in [
                "//button[contains(.,'Apply now') and not(contains(.,'company'))]",
                "//button[contains(.,'Easy Apply')]",
                "//span[contains(.,'Apply now')]/..",
                "[data-testid='indeedApplyButton']",
                ".ia-IndeedApplyButton",
                "button[id*='indeedApplyButton']",
            ]:
                try:
                    by = By.XPATH if sel.startswith("//") or sel.startswith("(") else By.CSS_SELECTOR
                    easy_apply_btn = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((by, sel))
                    )
                    break
                except TimeoutException:
                    pass

            if not easy_apply_btn:
                log.append({
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "job_id": job_id, "title": act_title, "company": company,
                    "status": "skipped_external", "url": cur_url,
                    "search_keyword": title,
                })
                save_log(log)
                print(f"    [{i+1}] Skip (external apply): {act_title[:40]} @ {company[:25]}")
                continue

            safe_click(driver, easy_apply_btn)
            time.sleep(2.5)

            result = handle_easy_apply(driver, job_id, act_title, company)

            log.append({
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "job_id": job_id, "title": act_title, "company": company,
                "status": result, "url": cur_url,
                "search_keyword": title,
            })
            save_log(log)

            if result == "submitted":
                applied_count += 1
                print(f"    [{i+1}] APPLIED: {act_title[:40]} @ {company[:25]}")
            else:
                print(f"    [{i+1}] {result}: {act_title[:40]} @ {company[:25]}")

            # Close modal if still open
            for close_sel in [
                "button[aria-label='Close']", "button[data-testid='modal-close']",
                ".css-1vg6q84", "[aria-label='close']"
            ]:
                try:
                    driver.find_element(By.CSS_SELECTOR, close_sel).click()
                    time.sleep(0.5)
                    break
                except Exception:
                    pass

            time.sleep(1)

        except StaleElementReferenceException:
            print(f"    [{i+1}] Stale element — skipping")
        except Exception as e:
            print(f"    [{i+1}] Error: {str(e)[:80]}")

    return applied_count

# ─── MAIN ──────────────────────────────────────────────────────
def main():
    print("=" * 60)
    print("  Indeed Auto-Apply — Harsh Madan")
    print("  Date:", datetime.now().strftime("%Y-%m-%d %H:%M"))
    print("=" * 60)

    log = load_log()
    print(f"  Previously applied: {len(log)} jobs\n")

    # Close any running Chrome (needed to attach to main profile)
    print("  Closing Chrome...")
    os.system("taskkill /f /im chrome.exe /t 2>nul")
    os.system("taskkill /f /im chromedriver.exe /t 2>nul")
    time.sleep(4)

    driver = get_driver()
    summary = {
        "date":          datetime.now().strftime("%Y-%m-%d"),
        "per_title":     {},
        "total_applied": 0,
        "status":        "completed",
        "errors":        [],
    }

    try:
        # Login
        if not indeed_google_login(driver):
            print("ERROR: Could not log in to Indeed.")
            summary["status"] = "login_failed"
            return

        total = 0
        for title in JOB_TITLES:
            try:
                count = search_and_apply(driver, title, log)
                summary["per_title"][title] = count
                total += count
                time.sleep(3)
            except Exception as e:
                err = f"{title}: {str(e)[:120]}"
                summary["errors"].append(err)
                summary["per_title"][title] = 0
                print(f"  ERROR in '{title}': {e}")

        summary["total_applied"] = total

    except Exception as e:
        summary["status"] = "error"
        summary["errors"].append(str(e))
        print(f"  FATAL ERROR: {e}")
    finally:
        try:
            driver.quit()
        except Exception:
            pass

    # Save summary
    summaries = []
    if os.path.exists(SUMMARY_FILE):
        with open(SUMMARY_FILE, encoding="utf-8") as f:
            summaries = json.load(f)
    summaries.append(summary)
    with open(SUMMARY_FILE, "w", encoding="utf-8") as f:
        json.dump(summaries, f, indent=2, ensure_ascii=False)

    print(f"\n{'='*60}")
    print(f"  INDEED RESULTS")
    print(f"  Total applied : {summary['total_applied']}")
    for t, c in summary["per_title"].items():
        print(f"    {t[:45]:<45} : {c}")
    if summary["errors"]:
        print(f"  Errors: {summary['errors']}")
    print(f"  Log saved     : {LOG_FILE}")
    print(f"  Summary saved : {SUMMARY_FILE}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
