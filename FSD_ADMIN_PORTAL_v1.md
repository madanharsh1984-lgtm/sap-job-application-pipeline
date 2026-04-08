# =============================================================================
# ADMIN_PORTAL_v1 — Functional Specification Document (FSD)
# =============================================================================
# Module: Admin Control Panel
# Version: 1.0
# Status: IMPLEMENTED
# =============================================================================

## 1. OVERVIEW

The Admin Portal is a RESTRICTED internal system providing complete visibility,
control, and monitoring over the SAP Job Application Pipeline SaaS platform.

**Scope:** Users, Payments, Job Activity, System Health, AI Automation Behavior.

---

## 2. ARCHITECTURE

```
┌─────────────────────────────────────────────────────────┐
│                   ADMIN PORTAL v1                       │
├─────────────────────────────────────────────────────────┤
│  Frontend (HTML/CSS/JS)  ←→  Flask API  ←→  SQLite DB  │
│                                                         │
│  Auth: JWT + Role-based (ADMIN only)                    │
│  Entry: run_admin.py → http://localhost:5000            │
└─────────────────────────────────────────────────────────┘
```

---

## 3. DATABASE SCHEMA

| Table               | Purpose                                      |
|---------------------|----------------------------------------------|
| `users`             | All platform users with role, status, limits  |
| `user_integrations` | Connected platforms (LinkedIn, Naukri, etc.)  |
| `resumes`           | Uploaded/generated resumes per user           |
| `jobs`              | All scraped job listings                      |
| `applications`      | All applications sent (with failure tracking) |
| `payments`          | Razorpay transactions and subscriptions       |
| `system_logs`       | Scraper status, API failures, queue backlog   |
| `ai_logs`           | AI decision tracking (keywords, matching)     |
| `admin_settings`    | Global configuration (pause, limits, freq)    |

### 3.1 Entity Relationships

```
users 1──N user_integrations
users 1──N resumes
users 1──N applications
users 1──N payments
users 1──N ai_logs
jobs  1──N applications
```

---

## 4. API SPECIFICATION

### 4.1 Authentication
| Method | Endpoint             | Description                          |
|--------|----------------------|--------------------------------------|
| POST   | /admin/auth/login    | Admin login → JWT token              |
| POST   | /admin/auth/setup    | First-time admin account creation    |

### 4.2 Dashboard
| Method | Endpoint                  | Description                     |
|--------|---------------------------|---------------------------------|
| GET    | /admin/dashboard-metrics  | Real-time KPI metrics           |

### 4.3 User Management
| Method | Endpoint                        | Description                   |
|--------|---------------------------------|-------------------------------|
| GET    | /admin/users                    | List/search/filter users      |
| GET    | /admin/user/{id}                | Detailed user profile         |
| POST   | /admin/user/disable             | Activate/deactivate user      |
| POST   | /admin/user/reset-integrations  | Reset user platform links     |
| GET    | /admin/user/{id}/logs           | User activity logs            |
| POST   | /admin/user/set-limit           | Set daily application limit   |

### 4.4 Payment Management
| Method | Endpoint               | Description                      |
|--------|------------------------|----------------------------------|
| GET    | /admin/payments        | List all transactions            |
| POST   | /admin/payment/refund  | Manual refund trigger            |
| POST   | /admin/payment/flag    | Flag/unflag suspicious activity  |

### 4.5 Job & Application Tracking
| Method | Endpoint              | Description                       |
|--------|-----------------------|-----------------------------------|
| GET    | /admin/jobs           | List scraped jobs by platform     |
| GET    | /admin/applications   | List applications with failures   |

### 4.6 System Monitoring
| Method | Endpoint            | Description                         |
|--------|---------------------|-------------------------------------|
| GET    | /admin/system-logs  | Filtered system/error logs          |
| GET    | /admin/ai-logs      | AI decision tracking logs           |

### 4.7 Control Panel
| Method | Endpoint              | Description                       |
|--------|-----------------------|-----------------------------------|
| POST   | /admin/system/pause   | Pause/resume automation           |
| GET    | /admin/settings       | Get all admin settings            |
| PUT    | /admin/settings       | Update admin settings             |

---

## 5. SECURITY

- All `/admin/*` API routes require JWT Bearer token
- Role validation: Only users with `role = "admin"` can access
- JWT secret configurable via `ADMIN_JWT_SECRET` environment variable
- Admin APIs are NEVER exposed publicly (localhost only by default)
- Password hashing via Werkzeug (PBKDF2)

---

## 6. UI PAGES

| Page               | Route         | Features                                |
|--------------------|---------------|-----------------------------------------|
| Login              | /             | Login + first-time admin setup          |
| Dashboard          | /dashboard    | 9 real-time KPI metric cards            |
| Users              | /users        | Search, filter, view, activate/disable  |
| Payments           | /payments     | Transaction list, refund, flag          |
| Jobs & Applications| /jobs         | Job list, application tracking, failures|
| System Logs        | /system-logs  | Filtered log viewer                     |
| Settings           | /settings     | Global pause, limits, frequency         |

---

## 7. METRICS TRACKED

### Dashboard Metrics
1. Total Users
2. Active Users (Daily)
3. Active Users (Weekly)
4. Total Jobs Discovered
5. Total Applications Sent
6. Failed Applications (critical)
7. Conversion Rate (Applications / Jobs)
8. Revenue Daily
9. Revenue Monthly

### Application Failure Reasons
- `email_not_found` — Recruiter email not available
- `apply_failed` — Application submission error
- `captcha` — CAPTCHA/bot detection blocked
- `blocked` — Platform blocked the account

---

## 8. ADMIN CONTROLS

| Control                       | Scope    | Description                           |
|-------------------------------|----------|---------------------------------------|
| Pause ALL automation          | Global   | Stops all scraping and applications   |
| Pause per user                | User     | Stops automation for specific user    |
| Daily application limit       | User     | Cap daily applications per user       |
| Scraping frequency            | Global   | Control how often scrapers run        |
| Activate/Deactivate user      | User     | Enable/disable user accounts          |
| Reset integrations            | User     | Reset platform connections            |

---

## 9. FAIL-SAFE RULES

- All admin actions are logged to `system_logs`
- Critical errors trigger `level = "critical"` log entries
- Data mismatch detection via metric validation
- Admin alerting via system log monitoring

---

## 10. DEPLOYMENT

```bash
# Install dependencies
pip install -r requirements.txt

# Set JWT secret (production)
export ADMIN_JWT_SECRET="your-secure-secret-key"

# Run admin portal
python run_admin.py

# Access at http://localhost:5000
# First visit: Create admin account via setup form
```

---

## 11. FILES

```
admin_portal/
├── __init__.py          # Package init
├── app.py               # Flask application factory
├── models.py            # Database schema (SQLAlchemy models)
├── routes.py            # API routes + page routes
├── templates/           # HTML templates
│   ├── login.html       # Login / setup page
│   ├── dashboard.html   # Dashboard with metrics
│   ├── users.html       # User management
│   ├── payments.html    # Payment management
│   ├── jobs.html        # Jobs & applications tracking
│   ├── system_logs.html # System log viewer
│   └── settings.html    # Settings & controls
└── static/
    ├── css/admin.css     # Styles
    └── js/admin.js       # Frontend logic

run_admin.py             # Entry point
requirements.txt         # Dependencies
FSD_ADMIN_PORTAL_v1.md   # This document
```
