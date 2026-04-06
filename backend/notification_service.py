import smtplib
import random
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import whatsapp_service

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GMAIL_USER = "Madan.harsh1984@gmail.com"
GMAIL_PASS = "hvaqnirvdvtkvofb"

def send_otp_email(to_email, otp_code):
    # Debug: Always log the attempt
    print(f"DEBUG: Preparing email to {to_email} from {GMAIL_USER} via SMTP...")
    
    try:
        msg = MIMEMultipart()
        msg['From'] = f"JobAccelerator AI <{GMAIL_USER}>"
        msg['To'] = to_email
        msg['Subject'] = "JobAccelerator AI - Verification Code"
        
        body = f"""
        Hello,
        
        Your verification code for JobAccelerator AI is: {otp_code}
        
        Please enter this code in the app to verify your identity.
        
        Best regards,
        JobAccelerator AI Team
        """
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(GMAIL_USER, GMAIL_PASS)
        server.send_message(msg)
        server.quit()
        print(f"SUCCESS: OTP email sent to {to_email}")
        return True
    except Exception as e:
        print(f"CRITICAL ERROR: Failed to send email to {to_email}: {str(e)}")
        with open(os.path.join(BASE_DIR, "notification_errors.log"), "a", encoding="utf-8") as f:
            f.write(f"[{datetime.datetime.now()}] EMAIL_ERROR: {to_email} | {str(e)}\n")
        return False

def send_otp_whatsapp(to_phone, otp_code):
    """Calls the JobAccelerator WhatsApp Test API."""
    normalized_phone = whatsapp_service.normalize_phone_number(to_phone)
    if not normalized_phone:
        print("ERROR: Cannot send WhatsApp OTP, phone number is missing")
        return False
    print(f"DEBUG: Calling send_otp_whatsapp for {normalized_phone} with code {otp_code}")
    return whatsapp_service.send_whatsapp_otp(normalized_phone, otp_code)

def generate_otp():
    return str(random.randint(100000, 999999))
