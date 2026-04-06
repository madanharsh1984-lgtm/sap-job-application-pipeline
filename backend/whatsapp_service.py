import datetime
import os

WHATSAPP_SENDER = "+919667964756"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "whatsapp_api.log")
LATEST_FILE = os.path.join(BASE_DIR, "latest_whatsapp_otp.txt")


def normalize_phone_number(phone: str | None) -> str:
    if not phone:
        return ""

    cleaned = "".join(ch for ch in phone if ch.isdigit() or ch == "+").strip()
    if not cleaned:
        return ""

    if cleaned.startswith("+"):
        return cleaned

    if len(cleaned) == 10:
        return f"+91{cleaned}"

    return f"+{cleaned}"


def send_whatsapp_otp(to_phone, otp_code):
    """
    Sends WhatsApp OTP using a simulated Test API.
    """
    normalized_phone = normalize_phone_number(to_phone)
    if not normalized_phone:
        print("ERROR: Failed to send WhatsApp OTP because phone number is empty or invalid")
        return False

    message = f"Your JobAccelerator AI verification code is: {otp_code}"
    print(f"DEBUG: Preparing log entry for {normalized_phone} with code {otp_code}")

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = (
        f"[{timestamp}] [SIMULATION] FROM: {WHATSAPP_SENDER} | TO: {normalized_phone} | "
        f"MESSAGE: {message} | STATUS: DELIVERED\n"
    )

    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_entry)
        print(f"SUCCESS: WhatsApp message logged to {LOG_FILE}")

        with open(LATEST_FILE, "w", encoding="utf-8") as f:
            f.write(f"{normalized_phone}:{otp_code}")
        print(f"SUCCESS: Latest OTP logged to {LATEST_FILE}")

        return True
    except Exception as e:
        print(f"ERROR: Failed to write to WhatsApp log: {str(e)}")
        return True
