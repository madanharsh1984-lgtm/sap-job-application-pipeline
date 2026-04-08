# AI Job Automation SaaS

Multi-tenant SaaS platform that automatically discovers, qualifies, and applies to jobs across multiple platforms using AI.

> **Governance:** All features are tracked in [`docs/FSD_v1.json`](docs/FSD_v1.json) — the single source of truth.

---

## Architecture

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Backend API** | Python / FastAPI | REST API, auth, business logic |
| **Database** | PostgreSQL | Users, jobs, applications |
| **Queue** | Redis | Background job processing |
| **Scraping** | Apify / JobSpy / Selenium | Multi-platform job discovery |
| **Frontend** | (planned) React / Vite | Dashboard, onboarding, settings |

## Project Structure

```
├── docs/
│   └── FSD_v1.json             ← Functional Specification Document (single source of truth)
│
├── backend/
│   ├── app/
│   │   ├── api/routes/         ← FastAPI route handlers (auth, jobs)
│   │   ├── core/               ← Config, security, database
│   │   ├── models/             ← SQLAlchemy ORM models (User, Job, Application)
│   │   ├── schemas/            ← Pydantic request/response schemas
│   │   ├── services/           ← Business logic
│   │   └── workers/            ← Background scraping & apply workers
│   ├── tests/                  ← Backend test suite
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
│
├── frontend/                   ← (planned) React dashboard
│
├── docker-compose.yml          ← Local dev: API + PostgreSQL + Redis
│
├── *.py                        ← Legacy pipeline scripts (being wrapped as workers)
├── *.bat                       ← Legacy Windows automation scripts
└── README.md
```

---

## Quick Start (Local Development)

### Option A — Docker Compose (recommended)

```bash
docker compose up -d
# API available at http://localhost:8000
# Swagger docs at http://localhost:8000/docs
```

### Option B — Manual

```bash
# 1. Start PostgreSQL and Redis locally

# 2. Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill in values
uvicorn app.main:app --reload

# 3. Legacy pipeline (optional)
pip install python-jobspy selenium webdriver-manager python-docx requests
cp config.example.py config.py  # fill in values
python apify_scrape.py
```

---

## Core Modules (FSD_v1)

| ID | Module | Status | Priority |
|----|--------|--------|----------|
| M1 | Job Discovery Engine | MVP | P0 |
| M2 | Application Engine | MVP | P0 |
| M3 | Resume Optimization Engine | MVP | P0 |
| M4 | User Experience Flow (Auth, Onboarding, Dashboard) | MVP | P0 |
| M5 | Monetization Flow (Razorpay) | MVP | P1 |
| M6 | Admin / Intelligence Engine | Post-MVP | P2 |

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| POST | `/api/v1/auth/signup` | Register new user |
| POST | `/api/v1/auth/login` | Login → JWT token |
| POST | `/api/v1/auth/forgot-password` | Request password reset |
| GET | `/api/v1/jobs` | List jobs (filters: source, remote_only) |
| GET | `/api/v1/jobs/dashboard` | Dashboard summary |

---

## Deployment Strategy

| Environment | Purpose | Status |
|-------------|---------|--------|
| Local | Development | ✅ Active |
| Staging | Beta (100 users) | 🔜 Planned |
| Production | 10K+ users | 🔜 Planned |

Pipeline: Dev → Staging → Production (no direct production push)

---

## Security

- **`config.py`** / **`.env`** — never committed. Contains all passwords and API tokens.
- **`apify_accounts.json`** — never committed. Contains Apify account tokens.
- **`email_sent_log.json`** — never committed. Contains recruiter emails.
- **Resume `.docx` files** — never committed. Share separately.
- **`.gitignore`** enforces all of the above automatically.
- OAuth for platform integrations (LinkedIn, Naukri, Indeed).
- User credentials encrypted at rest (AES-256).

---

## Legacy Pipeline Scripts

The original single-user automation scripts remain in the project root and are being progressively wrapped as multi-tenant background workers in `backend/app/workers/`.

| Script | Channel | Purpose |
|--------|---------|---------|
| `brightdata_scrape.py` | LinkedIn | Job scraping via Bright Data API |
| `jobspy_scrape.py` | LinkedIn/Indeed | Free job scraping via JobSpy |
| `apify_scrape.py` | LinkedIn | Recruiter post search via Apify |
| `send_sap_emails.py` | Email | Cold outreach to recruiters |
| `linkedin_easy_apply.py` | LinkedIn | Easy Apply automation |
| `naukri_auto_apply.py` | Naukri | Auto-apply automation |
| `indeed_auto_apply.py` | Indeed | Easy Apply automation |
| `resume_builder.py` | — | ATS-optimized resume generation |
| `headhunter_outreach.py` | Email | Headhunter firm targeting |
| `company_outreach.py` | Email | Direct CIO/VP outreach |
| `telegram_monitor.py` | Telegram | Job channel monitoring |
| `linkedin_autoposter.py` | LinkedIn | Thought leadership posts |
