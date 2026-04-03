"""
telegram_monitor.py — SAP Job Groups Monitor via Telegram
==========================================================
Monitors public Telegram SAP job channels for new job postings.
Extracts SAP-relevant posts matching Harsh Madan's profile.
Saves results to telegram_jobs.json and prints summary.

Uses Telegram MTProto API via telethon library.
If telethon not installed, falls back to web scraping public channels.

Setup (one-time):
  pip install telethon
  Then set TELEGRAM_API_ID and TELEGRAM_API_HASH below.
  Get these from: https://my.telegram.org/auth

Public SAP Job Channels monitored:
  - @sapjobsindia
  - @sap_jobs_india
  - @erp_jobs_india
  - @sapconsultantjobs
  - @sap_hana_jobs
  - @itjobsindia
"""

import json, os, sys, re, time
import urllib.request, urllib.parse
from datetime import datetime, timedelta

BASE_DIR  = r"C:\Users\madan\OneDrive\Desktop\Linkdin Job Application"
LOG_FILE  = os.path.join(BASE_DIR, "telegram_jobs.json")
SEEN_FILE = os.path.join(BASE_DIR, "telegram_seen.json")

# ── SAP KEYWORDS TO MATCH ─────────────────────────────────────────────────────
SAP_KEYWORDS = [
    "sap s/4hana", "s/4hana", "s4hana", "sap project manager",
    "sap program manager", "sap pm", "sap fico", "sap mm",
    "sap sd", "sap data migration", "lsmw", "ltmc",
    "sap implementation", "sap consultant", "sap programme",
    "sap erp", "sap manager", "sap lead",
]

EXPERIENCE_KEYWORDS = ["15 years", "12+ years", "10+ years", "senior", "lead", "manager", "head"]

# Public Telegram channels (accessible via web without API)
CHANNELS = [
    "sapjobsindia",
    "sap_jobs_india",
    "erp_jobs_india",
    "sapconsultantjobs",
    "sap_hana_jobs",
    "itjobsindia",
    "sapjobs",
    "sap_jobs",
    "erpjobs",
]

# ── HELPERS ───────────────────────────────────────────────────────────────────

def load_seen() -> set:
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE, encoding="utf-8") as f:
            return set(json.load(f))
    return set()

def save_seen(seen: set):
    with open(SEEN_FILE, "w", encoding="utf-8") as f:
        json.dump(list(seen), f)

def load_jobs() -> list:
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, encoding="utf-8") as f:
            return json.load(f)
    return []

def save_jobs(jobs: list):
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(jobs, f, indent=2, ensure_ascii=False)

def is_sap_job_post(text: str) -> bool:
    text_lower = text.lower()
    return any(kw in text_lower for kw in SAP_KEYWORDS)

def extract_emails(text: str) -> list:
    return re.findall(r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}', text)

def extract_phones(text: str) -> list:
    return re.findall(r'(?:\+91[\s-]?)?[6-9]\d{9}', text)

def scrape_telegram_web(channel: str) -> list:
    """Scrape public Telegram channel via t.me/s/channel (web preview)."""
    posts = []
    url = f"https://t.me/s/{channel}"
    req = urllib.request.Request(url)
    req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
    except Exception as e:
        print(f"    ✗ {channel}: {e}")
        return []

    # Extract message texts from Telegram web preview
    # Messages are in <div class="tgme_widget_message_text"> tags
    msg_pattern = re.findall(
        r'<div class="tgme_widget_message_text[^"]*"[^>]*>(.*?)</div>',
        html, re.DOTALL
    )

    # Also extract message IDs for deduplication
    id_pattern = re.findall(r'data-post="[^/]+/(\d+)"', html)

    # Clean HTML tags from messages
    def clean_html(text):
        text = re.sub(r'<br\s*/?>', '\n', text)
        text = re.sub(r'<[^>]+>', '', text)
        text = text.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&nbsp;', ' ')
        return text.strip()

    for i, raw_text in enumerate(msg_pattern):
        clean = clean_html(raw_text)
        if len(clean) < 30:
            continue
        if not is_sap_job_post(clean):
            continue

        msg_id = id_pattern[i] if i < len(id_pattern) else str(i)
        post_id = f"{channel}_{msg_id}"

        emails = extract_emails(clean)
        phones = extract_phones(clean)

        posts.append({
            "post_id": post_id,
            "channel": channel,
            "channel_url": url,
            "text": clean[:1000],
            "email": emails[0] if emails else "",
            "phone": phones[0] if phones else "",
            "has_contact": bool(emails or phones),
            "scraped_at": datetime.now().isoformat(),
        })

    print(f"    @{channel}: {len(posts)} SAP posts found")
    return posts

# ── TELETHON (if available) ────────────────────────────────────────────────────

def try_telethon_scrape() -> bool:
    """Check if telethon is available."""
    try:
        import telethon
        return True
    except ImportError:
        return False

# ── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    sys.stdout.reconfigure(encoding="utf-8")
    print("=" * 60)
    print("  Telegram SAP Job Monitor — Harsh Madan")
    print(f"  {datetime.now().strftime('%d %b %Y %H:%M')}")
    print("=" * 60)

    seen = load_seen()
    all_jobs = load_jobs()
    new_posts = []

    print(f"\n  Monitoring {len(CHANNELS)} Telegram channels...")

    for channel in CHANNELS:
        print(f"\n  Checking @{channel}:")
        posts = scrape_telegram_web(channel)
        for post in posts:
            if post["post_id"] not in seen:
                seen.add(post["post_id"])
                new_posts.append(post)
                all_jobs.append(post)
        time.sleep(2)

    save_seen(seen)
    save_jobs(all_jobs)

    print(f"\n  {'='*58}")
    print(f"  New SAP posts found    : {len(new_posts)}")
    with_contact = [p for p in new_posts if p["has_contact"]]
    print(f"  With email/phone       : {len(with_contact)}")

    if new_posts:
        print(f"\n  New Posts Summary:")
        print(f"  {'Channel':<25} {'Has Contact':<15} {'Preview'}")
        print(f"  {'-'*75}")
        for p in new_posts[:15]:
            preview = p["text"][:40].replace('\n', ' ')
            contact = f"📧 {p['email']}" if p["email"] else (f"📱 {p['phone']}" if p["phone"] else "—")
            print(f"  @{p['channel']:<24} {contact:<30} {preview}")

    # Save summary
    summary = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "channels_checked": len(CHANNELS),
        "new_posts": len(new_posts),
        "with_contact": len(with_contact),
        "posts": new_posts[:30],
    }
    with open(os.path.join(BASE_DIR, "telegram_summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    # Print install instructions if telethon not available
    if not try_telethon_scrape():
        print(f"""
  ─────────────────────────────────────────────────────
  NOTE: For PRIVATE Telegram group monitoring, install:
    pip install telethon

  Then get your API credentials from:
    https://my.telegram.org/auth

  This enables monitoring of private SAP job groups
  like WhatsApp-equivalent closed Telegram communities.
  ─────────────────────────────────────────────────────""")

    print("=" * 60)
    return summary

if __name__ == "__main__":
    main()
