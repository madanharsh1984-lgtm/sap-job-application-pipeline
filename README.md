# JobAccelerator AI

**AI-Powered Job Application Pipeline — Production-Ready SaaS System**

A scalable, modular SaaS platform that automates job searching, application tracking, resume tailoring, and auto-applying to job postings. Built to support up to 10,000 users.

---

## Architecture

```
┌─────────────┐    ┌──────────────┐    ┌─────────────────┐
│   Frontend   │───▶│   Backend    │───▶│   PostgreSQL    │
│  (Next.js)   │    │  (FastAPI)   │    │    Database      │
│  Port 3000   │    │  Port 8000   │    │    Port 5432     │
└─────────────┘    └──────┬───────┘    └─────────────────┘
                          │
                    ┌─────▼──────┐    ┌─────────────────┐
                    │   Redis    │───▶│     Worker       │
                    │  (Queue)   │    │   (Celery)       │
                    │  Port 6379 │    │  Background Jobs │
                    └────────────┘    └────────┬────────┘
                                               │
                                      ┌────────▼────────┐
                                      │ Browser Service  │
                                      │  (Playwright)    │
                                      │   Port 9000      │
                                      └─────────────────┘
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 14 (App Router) + Tailwind CSS |
| Backend | FastAPI (Python 3.11) |
| Database | PostgreSQL 16 |
| Queue | Redis 7 + Celery 5 |
| Automation | Playwright (Chromium) |
| Storage | AWS S3 (mock locally) |
| Containers | Docker + Docker Compose |
| CI/CD | GitHub Actions |

---

## Project Structure

```
Root/
├── frontend/                  # Next.js frontend application
│   ├── src/
│   │   ├── app/              # App Router pages
│   │   │   ├── login/        # Login page
│   │   │   ├── signup/       # Signup page
│   │   │   ├── dashboard/    # Protected dashboard
│   │   │   │   ├── jobs/     # Job management
│   │   │   │   ├── applications/  # Application tracking
│   │   │   │   └── resumes/  # Resume management
│   │   │   └── admin/        # Admin panel
│   │   ├── components/       # Shared components
│   │   └── lib/              # API helpers
│   ├── Dockerfile
│   └── package.json
│
├── backend/                   # FastAPI backend application
│   ├── app/
│   │   ├── api/routes/       # API route handlers
│   │   │   ├── auth.py       # Authentication endpoints
│   │   │   ├── jobs.py       # Job CRUD endpoints
│   │   │   ├── applications.py  # Application endpoints
│   │   │   ├── resumes.py    # Resume endpoints
│   │   │   └── admin.py      # Admin endpoints
│   │   ├── core/             # Core configuration
│   │   │   ├── config.py     # Settings management
│   │   │   ├── database.py   # Database setup
│   │   │   └── security.py   # JWT + password hashing
│   │   ├── models/           # SQLAlchemy models
│   │   ├── schemas/          # Pydantic schemas
│   │   ├── services/         # Business logic services
│   │   └── tests/            # Pytest test suite
│   ├── alembic/              # Database migrations
│   ├── Dockerfile
│   └── requirements.txt
│
├── worker/                    # Celery background workers
│   ├── tasks/
│   │   ├── scraping.py       # Job scraping tasks
│   │   ├── resume.py         # Resume generation tasks
│   │   └── email_tasks.py    # Email notification tasks
│   ├── celery_app.py         # Celery configuration
│   ├── Dockerfile
│   └── requirements.txt
│
├── browser-service/           # Playwright automation service
│   ├── scrapers/
│   │   ├── base.py           # Abstract base scraper
│   │   ├── linkedin.py       # LinkedIn job scraper
│   │   └── indeed.py         # Indeed job scraper
│   ├── browser_pool.py       # Browser pool manager
│   ├── main.py               # FastAPI service
│   ├── Dockerfile
│   └── requirements.txt
│
├── infra/                     # Infrastructure configs
│   ├── docker-compose.prod.yml  # Production overrides
│   ├── nginx.conf             # Reverse proxy config
│   └── init.sql               # Database initialization
│
├── .github/workflows/
│   └── ci.yml                 # CI/CD pipeline
│
├── docker-compose.yml         # Development orchestration
├── .env                       # Environment variables (git-ignored)
└── README.md
```

---

## Database Schema

| Table | Description |
|-------|-------------|
| `users` | User accounts with roles (admin/user) |
| `jobs` | Scraped/tracked job postings |
| `applications` | Job application records |
| `resumes` | Resume files and metadata |
| `payments` | Payment/subscription records |
| `logs` | System activity logs |

---

## Quick Start (Local Development)

### Prerequisites

- Docker & Docker Compose
- Git

### 1. Clone and Configure

```bash
git clone <repository-url>
cd sap-job-application-pipeline

# Edit .env if needed (defaults work for local development)
```

### 2. Start All Services

```bash
docker-compose up --build
```

This starts:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Browser Service**: http://localhost:9000
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379

### 3. Verify Health

```bash
curl http://localhost:8000/health
curl http://localhost:9000/health
```

---

## Manual Service Run (Without Docker)

### Backend

```bash
cd backend
pip install -r requirements.txt
export DATABASE_URL=postgresql://postgres:postgres@localhost:5432/jobaccelerator
export REDIS_URL=redis://localhost:6379/0
export SECRET_KEY=dev-secret-key
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
NEXT_PUBLIC_API_URL=http://localhost:8000 npm run dev
```

### Worker

```bash
cd worker
pip install -r requirements.txt
export REDIS_URL=redis://localhost:6379/0
celery -A worker.celery_app worker --loglevel=info
```

### Browser Service

```bash
cd browser-service
pip install -r requirements.txt
playwright install chromium
uvicorn main:app --port 9000
```

---

## API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register new user |
| POST | `/api/auth/login` | Login (returns JWT) |
| GET | `/api/auth/me` | Get current user |

### Jobs
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/jobs/` | List user's jobs |
| POST | `/api/jobs/` | Create job |
| GET | `/api/jobs/{id}` | Get job details |
| PUT | `/api/jobs/{id}` | Update job |
| DELETE | `/api/jobs/{id}` | Delete job |

### Applications
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/applications/` | List applications |
| POST | `/api/applications/` | Create application |
| GET | `/api/applications/{id}` | Get application |
| PUT | `/api/applications/{id}` | Update application |

### Resumes
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/resumes/` | List resumes |
| POST | `/api/resumes/upload` | Upload resume |
| GET | `/api/resumes/{id}` | Get resume |
| DELETE | `/api/resumes/{id}` | Delete resume |

### Admin (Admin role required)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/admin/users` | List all users |
| GET | `/api/admin/users/{id}` | Get user details |
| PUT | `/api/admin/users/{id}/role` | Update user role |
| GET | `/api/admin/stats` | System statistics |
| GET | `/api/admin/logs` | System logs |

---

## Production Deployment

### 1. Configure Environment

```bash
# Generate a secure secret key
export SECRET_KEY=$(openssl rand -hex 32)

# Update .env with production values
# - Set strong POSTGRES_PASSWORD
# - Set real AWS credentials for S3
# - Set SMTP credentials for email
```

### 2. Deploy with Production Overrides

```bash
docker-compose -f docker-compose.yml -f infra/docker-compose.prod.yml up -d --build
```

### 3. Run Database Migrations

```bash
docker-compose exec backend alembic upgrade head
```

### 4. Scale Workers

```bash
docker-compose -f docker-compose.yml -f infra/docker-compose.prod.yml up -d --scale worker=4
```

---

## CI/CD Pipeline

The GitHub Actions workflow (`.github/workflows/ci.yml`) runs:

1. **Backend Tests**: Lint + pytest with PostgreSQL/Redis services
2. **Frontend Build**: npm lint + build
3. **Docker Build**: Build images for all services
4. **Deploy**: Push to GitHub Container Registry (on main branch)

---

## Security

- **JWT Authentication**: All API endpoints (except auth) require valid JWT tokens
- **Password Hashing**: bcrypt via passlib
- **Role-Based Access**: Admin/User roles with middleware enforcement
- **Environment Variables**: All secrets via `.env` (git-ignored)
- **CORS**: Configurable allowed origins

---

## Legacy Pipeline Scripts

The root directory contains legacy automation scripts from the original SAP Job Application Pipeline. These scripts remain functional independently:

- `apify_scrape.py` — LinkedIn recruiter post scraping
- `linkedin_easy_apply.py` — LinkedIn auto-apply
- `naukri_auto_apply.py` — Naukri auto-apply
- `send_sap_emails.py` — Email outreach
- `resume_builder.py` — ATS resume builder

See `config.example.py` for legacy script configuration.

---

## License

Private — All rights reserved.
