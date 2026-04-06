import sys
import os

# Add backend to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import whatsapp_service

def test_whatsapp():
    print("Testing WhatsApp service...")
    result = whatsapp_service.send_whatsapp_otp("+919667964756", "999999")
    if result:
        print("Test SUCCESS")
    else:
        print("Test FAILED")

if __name__ == "__main__":
    test_whatsapp()
