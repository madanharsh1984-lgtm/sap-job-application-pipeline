import stripe
import os
from dotenv import load_dotenv

load_dotenv()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

def create_checkout_session(user_id: str, email: str, plan_price_id: str):
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': plan_price_id,
                    'quantity': 1,
                },
            ],
            mode='subscription',
            success_url='https://sap-job-monitor.com/dashboard?success=true',
            cancel_url='https://sap-job-monitor.com/billing?canceled=true',
            customer_email=email,
            metadata={
                "user_id": user_id
            }
        )
        return checkout_session.url
    except Exception as e:
        print(f"Stripe Checkout Error: {str(e)}")
        return None

def verify_webhook(payload: bytes, sig_header: str):
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
        return event
    except ValueError as e:
        # Invalid payload
        return None
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return None
