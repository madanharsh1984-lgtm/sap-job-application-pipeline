import pytest
from fastapi.testclient import TestClient
import uuid
from unittest.mock import patch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import sys
import tempfile

BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

# 1. Setup Mock Database for SIT
TEST_DB_PATH = os.path.join(tempfile.gettempdir(), f"jobaccelerator_test_{uuid.uuid4().hex}.db")
SQLALCHEMY_DATABASE_URL = f"sqlite:///{TEST_DB_PATH}"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 2. Patch database before importing app
with patch("database.SessionLocal", TestingSessionLocal), \
     patch("database.engine", engine):
    from main import app
    from database import Base, get_db
    import models

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture(scope="session", autouse=True)
def cleanup_test_db():
    yield
    engine.dispose()
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)

def test_sit_01_full_auth_flow():
    """Test Scenario SIT-01: End-to-End User Auth."""
    email = f"test_{uuid.uuid4().hex}@example.com"
    password = "securepassword123"
    
    # 1. Register
    reg_response = client.post("/auth/register", json={"email": email, "password": password})
    assert reg_response.status_code == 200
    
    # 2. Login
    login_response = client.post("/auth/login", data={"username": email, "password": password})
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    
    # 3. Access Protected Route
    headers = {"Authorization": f"Bearer {token}"}
    me_response = client.get("/user/me", headers=headers)
    assert me_response.status_code == 200
    assert me_response.json()["email"] == email

def test_sit_04_billing_webhook_flow():
    """Test Scenario SIT-04: Subscription/Payment Flow via Webhook."""
    email = f"billing_{uuid.uuid4().hex}@example.com"
    client.post("/auth/register", json={"email": email, "password": "pass"})
    db = TestingSessionLocal()
    user = db.query(models.User).filter(models.User.email == email).first()
    # UUID fix: pass the actual UUID object, not a string, for the filter
    user_id_obj = user.user_id 
    
    mock_payload = {
        "type": "checkout.session.completed",
        "data": {"object": {"metadata": {"user_id": str(user_id_obj)}}}
    }
    
    with patch("stripe_service.verify_webhook") as mock_verify:
        mock_verify.return_value = mock_payload
        response = client.post("/billing/webhook", json=mock_payload, headers={"stripe-signature": "mock"})
        assert response.status_code == 200
        
    db.refresh(user)
    assert user.subscription_tier == "Pro"
    db.close()

def test_sit_05_whatsapp_otp_logs_to_backend_directory():
    """Test Scenario SIT-05: WhatsApp OTP simulation writes to backend-owned files."""
    import whatsapp_service

    temp_log = os.path.join(tempfile.gettempdir(), f"whatsapp_log_{uuid.uuid4().hex}.log")
    temp_latest = os.path.join(tempfile.gettempdir(), f"whatsapp_latest_{uuid.uuid4().hex}.txt")
    original_log = whatsapp_service.LOG_FILE
    original_latest = whatsapp_service.LATEST_FILE
    whatsapp_service.LOG_FILE = temp_log
    whatsapp_service.LATEST_FILE = temp_latest

    try:
        phone = "96679 64756"
        otp = "123456"

        assert whatsapp_service.send_whatsapp_otp(phone, otp) is True
        assert os.path.exists(temp_log)
        assert os.path.exists(temp_latest)

        with open(temp_latest, "r", encoding="utf-8") as f:
            assert f.read().strip() == f"{whatsapp_service.normalize_phone_number(phone)}:{otp}"
    finally:
        whatsapp_service.LOG_FILE = original_log
        whatsapp_service.LATEST_FILE = original_latest
        for path in [temp_log, temp_latest]:
            if os.path.exists(path):
                os.remove(path)
