from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import timedelta, datetime
import models, schemas, database, stripe_service, security, tasks, notification_service
import uuid
import os
import random

app = FastAPI(title="JobAccelerator AI API")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3005",
        "http://127.0.0.1:3005",
        "http://[::1]:3005",
        "http://0.0.0.0:3005",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Database
models.Base.metadata.create_all(bind=database.engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@app.get("/")
def read_root():
    return {"message": "Welcome to JobAccelerator AI SaaS API"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "version": "1.2.0", "theme": "Midnight Navy & Cyber"}

@app.post("/auth/register", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    print(f"DEBUG: Received registration request: {user.dict()}")
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    normalized_phone = notification_service.whatsapp_service.normalize_phone_number(user.phone)

    if normalized_phone:
        db_phone = db.query(models.User).filter(models.User.phone == normalized_phone).first()
        if db_phone:
            raise HTTPException(status_code=400, detail="Phone number already registered")
    
    hashed_password = security.get_password_hash(user.password)
    
    # Generate OTPs
    email_otp = notification_service.generate_otp()
    phone_otp = notification_service.generate_otp()
    
    db_user = models.User(
        email=user.email, 
        password_hash=hashed_password,
        name=user.name,
        phone=normalized_phone or None,
        email_otp=email_otp,
        phone_otp=phone_otp,
        onboarding_step=0
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Send Email & WhatsApp OTP
    notification_service.send_otp_email(db_user.email, email_otp)
    notification_service.send_otp_whatsapp(db_user.phone, phone_otp)
    
    # Save for test automation
    with open(os.path.join(BASE_DIR, "latest_otp.txt"), "w", encoding="utf-8") as f:
        f.write(f"{db_user.email}:{email_otp}:{phone_otp}")
    
    return db_user

@app.post("/auth/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not security.verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/user/me", response_model=schemas.User)
def read_users_me(current_user: models.User = Depends(security.get_current_user)):
    return current_user

@app.patch("/user/me", response_model=schemas.User)
def update_user_me(user_update: schemas.UserUpdate, current_user: models.User = Depends(security.get_current_user), db: Session = Depends(database.get_db)):
    update_data = user_update.dict(exclude_unset=True)
    if "phone" in update_data:
        update_data["phone"] = notification_service.whatsapp_service.normalize_phone_number(update_data["phone"]) or None
    for key, value in update_data.items():
        setattr(current_user, key, value)
    db.commit()
    db.refresh(current_user)
    return current_user

@app.post("/auth/verify-phone")
def verify_phone(verify: schemas.OTPVerify, current_user: models.User = Depends(security.get_current_user), db: Session = Depends(database.get_db)):
    if verify.code == current_user.phone_otp: 
        current_user.is_phone_verified = True
        if current_user.is_phone_verified and current_user.is_email_verified and current_user.onboarding_step < 1:
            current_user.onboarding_step = 1
        db.commit()
        return {"msg": "Phone verified successfully"}
    raise HTTPException(status_code=400, detail="Invalid verification code")

@app.post("/auth/verify-email")
def verify_email(verify: schemas.EmailVerify, current_user: models.User = Depends(security.get_current_user), db: Session = Depends(database.get_db)):
    if verify.code == current_user.email_otp:
        current_user.is_email_verified = True
        if current_user.is_phone_verified and current_user.is_email_verified and current_user.onboarding_step < 1:
            current_user.onboarding_step = 1
        db.commit()
        return {"msg": "Email verified successfully"}
    raise HTTPException(status_code=400, detail="Invalid verification code")

@app.post("/auth/resend-otp")
def resend_otp(current_user: models.User = Depends(security.get_current_user), db: Session = Depends(database.get_db)):
    email_otp = notification_service.generate_otp()
    phone_otp = notification_service.generate_otp()
    current_user.email_otp = email_otp
    current_user.phone_otp = phone_otp
    db.commit()
    notification_service.send_otp_email(current_user.email, email_otp)
    notification_service.send_otp_whatsapp(current_user.phone, phone_otp)
    return {"msg": "Verification codes resent"}

@app.post("/user/linkedin/evaluate")
def evaluate_linkedin(current_user: models.User = Depends(security.get_current_user), db: Session = Depends(database.get_db)):
    score = random.randint(65, 88)
    current_user.linkedin_profile_score = score
    db.commit()
    return {"score": score}

@app.post("/user/linkedin/optimize")
def optimize_linkedin(current_user: models.User = Depends(security.get_current_user), db: Session = Depends(database.get_db)):
    current_user.linkedin_profile_score = 98
    db.commit()
    return {"score": 98}

@app.post("/webhooks/fyltr")
async def fyltr_webhook(request: Request, db: Session = Depends(database.get_db)):
    payload = await request.json()
    email = payload.get("email")
    if not email:
        return {"status": "error", "message": "Email missing"}
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        return {"status": "error", "message": "User not found"}
    user.name = payload.get("full_name", user.name)
    user.phone = payload.get("phone", user.phone)
    user.onboarding_step = 2
    db.commit()
    return {"status": "success"}

@app.post("/billing/checkout")
def create_checkout_session(plan_id: str, current_user: models.User = Depends(security.get_current_user)):
    checkout_url = stripe_service.create_checkout_session(str(current_user.user_id), current_user.email, plan_id)
    if not checkout_url:
        raise HTTPException(status_code=500, detail="Failed to create checkout session")
    return {"checkout_url": checkout_url}

@app.post("/billing/webhook")
async def stripe_webhook(request: Request, db: Session = Depends(database.get_db)):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    event = stripe_service.verify_webhook(payload, sig_header)
    if not event:
        raise HTTPException(status_code=400, detail="Invalid webhook signature")
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        user_id_str = session.get('metadata', {}).get('user_id')
        if user_id_str:
            try:
                user_uuid = uuid.UUID(user_id_str)
                user = db.query(models.User).filter(models.User.user_id == user_uuid).first()
                if user:
                    user.subscription_tier = "Pro"
                    db.commit()
            except ValueError:
                pass
    return {"status": "success"}

@app.post("/applications", status_code=status.HTTP_202_ACCEPTED)
def apply_to_job(app_request: schemas.ApplicationCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(security.get_current_user)):
    lead = db.query(models.JobLead).filter(models.JobLead.lead_id == app_request.lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Job Lead not found")
    creds = db.query(models.UserCredential).filter(models.UserCredential.user_id == current_user.user_id, models.UserCredential.platform == lead.platform).first()
    if not creds:
        raise HTTPException(status_code=400, detail=f"No credentials found for {lead.platform}")
    tasks.tailor_and_apply.delay(str(current_user.user_id), str(app_request.lead_id), str(app_request.resume_id))
    return {"message": "Application task queued successfully."}

@app.get("/admin/whatsapp-logs")
def get_whatsapp_logs():
    log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "whatsapp_api.log")
    logs = []
    if os.path.exists(log_file):
        with open(log_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines:
                try:
                    parts = line.split(" | ")
                    if len(parts) >= 4:
                        ts = parts[0].split("] ")[0].replace("[", "")
                        from_num = parts[0].split("FROM: ")[1]
                        to_num = parts[1].split("TO: ")[1]
                        msg = parts[2].split("MESSAGE: ")[1]
                        status = parts[3].split("STATUS: ")[1].strip()
                        logs.append({
                            "timestamp": ts,
                            "from_num": from_num,
                            "to_num": to_num,
                            "message": msg,
                            "status": status
                        })
                except:
                    pass
    return logs[::-1][:50]
