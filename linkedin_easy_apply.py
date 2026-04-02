"""
LinkedIn Easy Apply Automation — Harsh Madan
=============================================
Searches LinkedIn Jobs for 4 SAP titles (Remote, Last 24h),
finds Easy Apply postings, auto-fills and submits applications.
Uses a fresh Chrome profile + Google OAuth login (email+password).
"""

import os, json, time, re, sys
from datetime import datetime
sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

from config import (
    RESUME_PATH, BASE_DIR, LOG_DIR,
    JOB_TITLES, CANDIDATE,
    GOOGLE_EMAIL, GOOGLE_PASS,
    LINKEDIN_EMAIL, LINKEDIN_PASS,
    CHROME_BIN, CHROMEDRIVER_PATH, CHROME_PROFILE_LI,
)

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException, NoSuchElementException,
    ElementNotInteractableException, StaleElementReferenceException
)

# ── CONFIG ────────────────────────────────────────────────────────
OUTPUT_FOLDER = BASE_DIR
LOG_FILE      = os.path.join(LOG_DIR, "applied_jobs_log.json")

# ── CHROME DRIVER ─────────────────────────────────────────────────
def get_driver():
    CHROMEDRIVER = CHROMEDRIVER_PATH
    TEMP_DIR     = CHROME_PROFILE_LI

    import shutil
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


# ── LINKEDIN LOGIN ─────────────────────────────────────────────────
def linkedin_login(driver):
    print("  Navigating to LinkedIn login...")
    driver.get("https://www.linkedin.com/login")
    time.sleep(4)

    # Already logged in?
    if "feed" in driver.current_url or (
        "linkedin.com" in driver.current_url
        and "login" not in driver.current_url
        and "authwall" not in driver.current_url
    ):
        print("  Already logged in.")
        return True

    # ── METHOD 1: Direct LinkedIn email + password (fastest) ──────
    try:
        email_field = WebDriverWait(driver, 8).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        email_field.clear()
        email_field.send_keys(LINKEDIN_EMAIL)
        pass_field = driver.find_element(By.ID, "password")
        pass_field.clear()
        pass_field.send_keys(LINKEDIN_PASS)
        pass_field.send_keys(Keys.RETURN)
        print("  Submitted LinkedIn email+password.")
        time.sleep(5)
        cur = driver.current_url
        if "feed" in cur or ("linkedin.com" in cur and "login" not in cur and "checkpoint" not in cur):
            print("  Direct LinkedIn login successful!")
            return True
        print(f"  Direct login result URL: {cur} — trying Google OAuth...")
    except Exception as e:
        print(f"  Direct login attempt: {e} — trying Google OAuth...")

    # Reload login page for Google OAuth
    driver.get("https://www.linkedin.com/login")
    time.sleep(3)

    # ── METHOD 2: Continue with Google (OAuth) ────────────────────
    # Try clicking 'Continue with Google'
    google_btn = None
    try:
        all_elems = driver.find_elements(By.XPATH, "//*[contains(translate(text(),'GOOGLE','google'),'google') or contains(translate(@aria-label,'GOOGLE','google'),'google')]")
        for el in all_elems:
            tag = el.tag_name.lower()
            if tag in ("a", "button", "div", "span"):
                google_btn = el
                print(f"  Found Google button: '{el.text.strip()[:40]}'")
                break
    except Exception:
        pass

    if not google_btn:
        # CSS fallbacks
        for css in ["a[href*='google']", "button[aria-label*='Google']",
                    "[data-litms-control-urn]", ".google-login-btn"]:
            try:
                google_btn = WebDriverWait(driver, 4).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, css))
                )
                break
            except Exception:
                pass

    if google_btn:
        try:
            driver.execute_script("arguments[0].scrollIntoView(true);", google_btn)
            time.sleep(0.5)
            try:
                google_btn.click()
            except Exception:
                driver.execute_script("arguments[0].click();", google_btn)
            print("  Clicked 'Continue with Google'.")
            time.sleep(4)

            # Handle Google OAuth popup
            original = driver.current_window_handle
            time.sleep(2)
            if len(driver.window_handles) > 1:
                for h in driver.window_handles:
                    if h != original:
                        driver.switch_to.window(h)
                        print(f"  Google popup: {driver.current_url}")
                        break
                time.sleep(2)

            # Enter email if asked
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

            # Enter password if asked
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
                    acct = WebDriverWait(driver, 4).until(
                        EC.element_to_be_clickable((By.XPATH, sel))
                    )
                    acct.click()
                    time.sleep(3)
                    break
                except Exception:
                    pass

            # Allow/consent
            for sel in ["//button[contains(.,'Allow')]", "//button[contains(.,'Continue')]",
                        "//button[contains(.,'Next')]"]:
                try:
                    WebDriverWait(driver, 4).until(
                        EC.element_to_be_clickable((By.XPATH, sel))
                    ).click()
                    time.sleep(3)
                    break
                except Exception:
                    pass

            # Switch back
            if len(driver.window_handles) > 1:
                driver.switch_to.window(original)
                time.sleep(3)

        except Exception as e:
            print(f"  Google OAuth error: {e}")

    # Check if logged in
    for _ in range(15):
        cur = driver.current_url
        if "feed" in cur or ("linkedin.com" in cur and "login" not in cur and "authwall" not in cur):
            print(f"  Logged in! URL: {cur}")
            return True
        time.sleep(1)

    # Save screenshot for debug
    try:
        driver.save_screenshot(os.path.join(OUTPUT_FOLDER, "linkedin_login_debug.png"))
    except Exception:
        pass

    print("  Login failed. Waiting 90s for manual login...")
    time.sleep(90)
    cur = driver.current_url
    return "feed" in cur or ("linkedin.com" in cur and "login" not in cur)


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
    return any(e.get("job_id") == job_id for e in log)


# ── FORM HELPERS ──────────────────────────────────────────────────
def fill_text(el, value):
    try:
        el.click()
        el.send_keys(Keys.CONTROL + "a")
        el.send_keys(Keys.DELETE)
        el.clear()
        el.send_keys(str(value))
    except Exception:
        pass

def safe_click(driver, el):
    try:
        el.click()
    except Exception:
        try:
            driver.execute_script("arguments[0].click();", el)
        except Exception:
            pass

def get_field_label(driver, field):
    """Extract label text for a form field."""
    label_text = ""
    try:
        fid = field.get_attribute("id") or ""
        if fid:
            lbls = driver.find_elements(By.CSS_SELECTOR, f"label[for='{fid}']")
            if lbls:
                label_text = lbls[0].text.lower()
        if not label_text:
            # Walk up DOM to find a label or fieldset legend
            try:
                parent = field.find_element(By.XPATH, "../..")
                label_text = parent.text.lower()
            except Exception:
                pass
    except Exception:
        pass
    placeholder = (field.get_attribute("placeholder") or "").lower()
    aria = (field.get_attribute("aria-label") or "").lower()
    return label_text + " " + placeholder + " " + aria


def fill_city_typeahead(driver, field, city_value):
    """
    Fill a LinkedIn city/location typeahead autocomplete field.
    Types the city, waits for the dropdown suggestion, clicks first match.
    """
    try:
        field.click()
        time.sleep(0.3)
        field.send_keys(Keys.CONTROL + "a")
        field.send_keys(Keys.DELETE)
        field.clear()
        time.sleep(0.3)
        # Type slowly to trigger autocomplete
        for ch in city_value[:6]:
            field.send_keys(ch)
            time.sleep(0.15)
        time.sleep(2)  # wait for dropdown to appear

        # Try to click first suggestion from the dropdown
        suggestion_clicked = False
        for dropdown_sel in [
            ".basic-typeahead__triggered-content li:first-child",
            ".search-typeahead-v2__hit",
            "div[role='option']:first-child",
            "li[role='option']:first-child",
            ".typeahead-result:first-child",
            ".fb-typeahead-item:first-child",
        ]:
            try:
                suggestion = WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, dropdown_sel))
                )
                suggestion.click()
                suggestion_clicked = True
                print(f"      City typeahead: clicked suggestion via {dropdown_sel}")
                time.sleep(0.5)
                break
            except Exception:
                pass

        if not suggestion_clicked:
            # Try XPath-based first option
            for xpath_sel in [
                "//div[@role='option'][1]",
                "//li[@role='option'][1]",
                "//*[contains(@class,'typeahead')]//li[1]",
                "//*[contains(@class,'suggestion')][1]",
            ]:
                try:
                    suggestion = WebDriverWait(driver, 2).until(
                        EC.element_to_be_clickable((By.XPATH, xpath_sel))
                    )
                    suggestion.click()
                    suggestion_clicked = True
                    print(f"      City typeahead: clicked via XPATH {xpath_sel}")
                    time.sleep(0.5)
                    break
                except Exception:
                    pass

        if not suggestion_clicked:
            # Final fallback: press Enter/Down+Enter to select first suggestion
            field.send_keys(Keys.ARROW_DOWN)
            time.sleep(0.3)
            field.send_keys(Keys.RETURN)
            print("      City typeahead: used Arrow+Enter fallback")
            time.sleep(0.5)
    except Exception as e:
        print(f"      City typeahead error: {e}")


def fill_easy_apply_form(driver):
    """Fill in all form fields on an Easy Apply modal page."""
    try:
        fields = driver.find_elements(By.CSS_SELECTOR,
            "input[type='text'], input[type='tel'], input[type='number'], textarea")
        for field in fields:
            try:
                if not field.is_displayed() or not field.is_enabled():
                    continue
                combined = get_field_label(driver, field)
                current = field.get_attribute("value") or ""

                # City / Location — special typeahead handling
                if ("city" in combined or "location" in combined
                        or "where" in combined) and "current" not in combined:
                    if not current.strip():
                        fill_city_typeahead(driver, field, "Delhi")
                    continue

                val = None
                if "phone" in combined or "mobile" in combined:
                    val = CANDIDATE["phone"]
                elif "year" in combined and ("experience" in combined or "exp" in combined):
                    val = CANDIDATE["years_exp"]
                elif "current" in combined and ("ctc" in combined or "salary" in combined
                                                or "compensation" in combined or "lpa" in combined):
                    val = CANDIDATE["current_ctc"]
                elif "expected" in combined and ("ctc" in combined or "salary" in combined
                                                 or "lpa" in combined):
                    val = CANDIDATE["expected_ctc"]
                elif "notice" in combined or "availability" in combined:
                    val = "0"
                elif "linkedin" in combined or "profile url" in combined:
                    val = CANDIDATE["linkedin"]
                elif ("first" in combined and "name" in combined):
                    val = "Harsh"
                elif ("last" in combined and "name" in combined):
                    val = "Madan"
                elif "name" in combined and "company" not in combined and "employer" not in combined:
                    val = CANDIDATE["name"]
                elif "website" in combined or "portfolio" in combined:
                    val = CANDIDATE["linkedin"]

                if val and not current.strip():
                    fill_text(field, val)
            except Exception:
                continue

        # Handle standard <select> dropdowns
        from selenium.webdriver.support.ui import Select as SeleniumSelect
        selects = driver.find_elements(By.TAG_NAME, "select")
        for sel_el in selects:
            try:
                if not sel_el.is_displayed():
                    continue
                sid = sel_el.get_attribute("id") or ""
                label_text = ""
                if sid:
                    lbls = driver.find_elements(By.CSS_SELECTOR, f"label[for='{sid}']")
                    if lbls:
                        label_text = lbls[0].text.lower()
                aria = (sel_el.get_attribute("aria-label") or "").lower()
                combined = label_text + " " + aria
                s = SeleniumSelect(sel_el)
                current_val = s.first_selected_option.text.strip().lower()
                if current_val in ("select an option", "", "select", "choose"):
                    if "notice" in combined or "availability" in combined:
                        try:
                            s.select_by_visible_text("Immediately")
                        except Exception:
                            try: s.select_by_index(1)
                            except Exception: pass
                    elif "experience" in combined or "years" in combined:
                        selected = False
                        for opt in s.options:
                            if any(x in opt.text for x in ("10+", "15+", "More than 10", "11-15", "16-20")):
                                opt.click(); selected = True; break
                        if not selected:
                            try: s.select_by_index(len(s.options) - 1)
                            except Exception: pass
                    elif "country" in combined or "work auth" in combined:
                        try:
                            s.select_by_visible_text("India")
                        except Exception:
                            try: s.select_by_index(1)
                            except Exception: pass
                    elif "yes" in [o.text.lower() for o in s.options]:
                        # Visa/sponsorship questions — answer Yes
                        try: s.select_by_visible_text("Yes")
                        except Exception: pass
            except Exception:
                continue

        # Handle radio buttons (Yes/No questions)
        try:
            radios = driver.find_elements(By.CSS_SELECTOR, "fieldset")
            for fieldset in radios:
                try:
                    legend = fieldset.find_element(By.TAG_NAME, "legend").text.lower()
                    # "do you require sponsorship" — answer No
                    if "sponsor" in legend:
                        try:
                            no_btn = fieldset.find_element(By.XPATH, ".//label[contains(translate(.,'NO','no'),'no')]")
                            no_btn.click()
                        except Exception:
                            pass
                    # "are you authorized to work" — answer Yes
                    elif "authoriz" in legend or "eligible" in legend or "legally" in legend:
                        try:
                            yes_btn = fieldset.find_element(By.XPATH, ".//label[contains(translate(.,'YES','yes'),'yes')]")
                            yes_btn.click()
                        except Exception:
                            pass
                except Exception:
                    continue
        except Exception:
            pass

    except Exception as e:
        print(f"    Form fill error: {e}")


# ── APPLY TO JOB ──────────────────────────────────────────────────
def apply_to_job(driver, job_card, log):
    """Click a job card, open Easy Apply, fill form, submit."""
    try:
        safe_click(driver, job_card)
        time.sleep(2)

        # Get job ID from URL or data attribute
        job_url = driver.current_url
        job_id_match = re.search(r"currentJobId=(\d+)|/jobs/view/(\d+)", job_url)
        if not job_id_match:
            try:
                job_id = job_card.get_attribute("data-job-id") or job_url
            except Exception:
                job_id = job_url
        else:
            job_id = job_id_match.group(1) or job_id_match.group(2)

        if already_applied(log, str(job_id)):
            print(f"    Already applied: {job_id}")
            return False

        # Get job title and company
        job_title = ""
        company = ""
        try:
            job_title = driver.find_element(By.CSS_SELECTOR, ".job-details-jobs-unified-top-card__job-title, h1.t-24").text.strip()
        except Exception:
            pass
        try:
            company = driver.find_element(By.CSS_SELECTOR, ".job-details-jobs-unified-top-card__company-name, .jobs-unified-top-card__company-name").text.strip()
        except Exception:
            pass

        # Find Easy Apply button
        easy_btn = None
        for btn_sel in [
            "//button[contains(.,'Easy Apply')]",
            "//button[contains(@aria-label,'Easy Apply')]",
            ".jobs-apply-button--top-card button",
        ]:
            try:
                if btn_sel.startswith("//"):
                    easy_btn = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, btn_sel))
                    )
                else:
                    easy_btn = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, btn_sel))
                    )
                break
            except Exception:
                pass

        if not easy_btn:
            return False

        safe_click(driver, easy_btn)
        print(f"    Opened Easy Apply: {job_title} @ {company}")
        time.sleep(2)

        # Step through modal pages
        for step in range(10):
            fill_easy_apply_form(driver)
            time.sleep(1)

            # Try Submit
            submitted = False
            for sub_sel in ["//button[contains(.,'Submit application')]",
                            "//button[contains(.,'Submit')]"]:
                try:
                    sub_btn = WebDriverWait(driver, 3).until(
                        EC.element_to_be_clickable((By.XPATH, sub_sel))
                    )
                    safe_click(driver, sub_btn)
                    submitted = True
                    print(f"    SUBMITTED: {job_title} @ {company}")
                    time.sleep(2)
                    break
                except Exception:
                    pass

            if submitted:
                # Dismiss confirmation
                for dismiss in ["//button[contains(.,'Done')]", "//button[@aria-label='Dismiss']"]:
                    try:
                        WebDriverWait(driver, 3).until(
                            EC.element_to_be_clickable((By.XPATH, dismiss))
                        ).click()
                        time.sleep(1)
                        break
                    except Exception:
                        pass
                log.append({
                    "job_id": str(job_id),
                    "job_title": job_title,
                    "company": company,
                    "job_url": job_url,
                    "applied_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "status": "Applied"
                })
                save_log(log)
                return True

            # Next page
            next_clicked = False
            for next_sel in ["//button[contains(.,'Next')]",
                             "//button[contains(.,'Continue')]",
                             "//button[contains(.,'Review')]"]:
                try:
                    next_btn = WebDriverWait(driver, 3).until(
                        EC.element_to_be_clickable((By.XPATH, next_sel))
                    )
                    safe_click(driver, next_btn)
                    next_clicked = True
                    time.sleep(2)
                    break
                except Exception:
                    pass

            if not next_clicked:
                # Dismiss and give up
                for dismiss in ["//button[@aria-label='Dismiss']", "//button[contains(.,'Discard')]"]:
                    try:
                        WebDriverWait(driver, 2).until(
                            EC.element_to_be_clickable((By.XPATH, dismiss))
                        ).click()
                        time.sleep(1)
                        break
                    except Exception:
                        pass
                break

        return False

    except Exception as e:
        print(f"    Apply error: {e}")
        return False


# ── SEARCH AND APPLY ──────────────────────────────────────────────
def search_and_apply(driver, title, log):
    applied = 0
    # Build search URL: remote, last 24h, easy apply
    # f_WT=2 = Remote, f_TPR=r86400 = last 24h, f_LF=f_AL = Easy Apply
    query = title.replace(" ", "%20")
    url = (f"https://www.linkedin.com/jobs/search/?keywords={query}"
           "&f_WT=2&f_TPR=r86400&f_LF=f_AL&sortBy=DD")
    print(f"  Searching: {title}")
    driver.get(url)
    time.sleep(4)

    # Scroll to load jobs
    last_height = 0
    for _ in range(3):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Get job cards
    cards = driver.find_elements(By.CSS_SELECTOR,
        ".job-card-container, .jobs-search-results__list-item, li.scaffold-layout__list-item")
    print(f"    Found {len(cards)} job cards.")

    for i, card in enumerate(cards[:20]):
        try:
            print(f"    Checking card {i+1}/{min(len(cards),20)}...")
            result = apply_to_job(driver, card, log)
            if result:
                applied += 1
            time.sleep(1)
        except Exception as e:
            print(f"    Card error: {e}")
            continue

    return applied


# ── MAIN ──────────────────────────────────────────────────────────
def main():
    print("=" * 55)
    print(f"  LinkedIn Easy Apply — Harsh Madan")
    print(f"  {datetime.now().strftime('%d %b %Y %H:%M')}")
    print("=" * 55)
    print(f"  Resume: {os.path.basename(RESUME_PATH)}")
    print(f"  Filters: Remote | Last 24h | Easy Apply only")
    print(f"  Job titles: {len(JOB_TITLES)}")
    print()

    if not os.path.exists(RESUME_PATH):
        print(f"ERROR: Resume not found: {RESUME_PATH}")
        return

    log = load_log()
    print(f"  Previously applied: {len(log)} jobs")
    print()

    # Kill any running Chrome
    print("  Closing any running Chrome instances...")
    os.system("taskkill /f /im chrome.exe /t 2>nul")
    os.system("taskkill /f /im chromedriver.exe /t 2>nul")
    time.sleep(4)

    driver = None
    try:
        driver = get_driver()
        print("  Chrome launched.")

        print("  Checking LinkedIn login status...")
        if not linkedin_login(driver):
            print("ERROR: Could not log in to LinkedIn. Exiting.")
            return

        total_applied = 0
        summary = {}

        for title in JOB_TITLES:
            count = search_and_apply(driver, title, log)
            summary[title] = count
            total_applied += count
            print(f"  [{title}] Applied: {count}")
            time.sleep(2)

        print()
        print("=" * 55)
        print(f"  DONE. Total applied: {total_applied}")
        for t, c in summary.items():
            print(f"    {t}: {c}")
        print("=" * 55)

        # Save summary
        with open(os.path.join(OUTPUT_FOLDER, "easy_apply_summary.json"), "w", encoding="utf-8") as f:
            json.dump({
                "date": datetime.now().strftime("%Y-%m-%d"),
                "total_applied": total_applied,
                "breakdown": summary
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
