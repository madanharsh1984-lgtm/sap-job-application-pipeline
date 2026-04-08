# Backend - AI Job Automation SaaS

FastAPI-based backend for the AI Job Automation SaaS platform.

## Structure

```
backend/
├── app/
│   ├── api/
│   │   └── routes/        # API route handlers
│   ├── core/              # Configuration, security, dependencies
│   ├── models/            # SQLAlchemy ORM models
│   ├── schemas/           # Pydantic request/response schemas
│   ├── services/          # Business logic layer
│   └── workers/           # Background job workers (scraping, applying)
├── tests/                 # Test suite
├── requirements.txt       # Python dependencies
└── Dockerfile             # Container image
```

## Quick Start

```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Environment Variables

Copy `.env.example` to `.env` and fill in the required values.
