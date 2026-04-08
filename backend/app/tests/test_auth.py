"""Tests for authentication endpoints."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db
from app.main import app

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    """Provide a test database session."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_tables():
    """Reset database tables between tests."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


def test_register_user():
    """Test that a new user can register successfully."""
    response = client.post(
        "/api/auth/register",
        json={
            "email": "test@example.com",
            "password": "securepassword123",
            "full_name": "Test User",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["full_name"] == "Test User"
    assert data["role"] == "user"
    assert "id" in data


def test_register_duplicate_email():
    """Test that registering with a duplicate email returns 400."""
    payload = {
        "email": "dup@example.com",
        "password": "securepassword123",
        "full_name": "Dup User",
    }
    client.post("/api/auth/register", json=payload)
    response = client.post("/api/auth/register", json=payload)
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]


def test_login_user():
    """Test that a registered user can log in and receive a token."""
    client.post(
        "/api/auth/register",
        json={
            "email": "login@example.com",
            "password": "securepassword123",
            "full_name": "Login User",
        },
    )
    response = client.post(
        "/api/auth/login",
        data={"username": "login@example.com", "password": "securepassword123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials():
    """Test that invalid credentials return 401."""
    response = client.post(
        "/api/auth/login",
        data={"username": "nobody@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 401


def test_get_current_user():
    """Test that an authenticated user can fetch their own profile."""
    client.post(
        "/api/auth/register",
        json={
            "email": "me@example.com",
            "password": "securepassword123",
            "full_name": "Me User",
        },
    )
    login_resp = client.post(
        "/api/auth/login",
        data={"username": "me@example.com", "password": "securepassword123"},
    )
    token = login_resp.json()["access_token"]
    response = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "me@example.com"
    assert data["full_name"] == "Me User"


def test_get_current_user_unauthenticated():
    """Test that accessing /me without a token returns 401."""
    response = client.get("/api/auth/me")
    assert response.status_code == 401
