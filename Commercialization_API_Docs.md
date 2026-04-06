# API Documentation: SAP Job Application SaaS Platform

This document outlines the core backend API endpoints (RESTful) for the SaaS platform.

## Base URL: `https://api.sap-job-monitor.com/v1/`

### 1. Authentication (`/auth`)
- **POST `/auth/register`**: User registration (email, password).
- **POST `/auth/login`**: User login (JWT-based).
- **POST `/auth/refresh`**: Refresh access token.
- **POST `/auth/logout`**: Invalidate session.
- **POST `/auth/mfa/enable`**: Enable Multi-Factor Authentication.

### 2. User & Profile (`/user`)
- **GET `/user/me`**: Get current user profile and settings.
- **PATCH `/user/me`**: Update profile (name, target job titles, keywords).
- **GET `/user/preferences`**: Get scraping & application preferences.
- **PATCH `/user/preferences`**: Update notification & automation settings.

### 3. Platform Credentials (`/credentials`)
- **GET `/credentials`**: List connected platforms (LinkedIn, Naukri, Gmail).
- **POST `/credentials/connect`**: Securely connect/update a platform's credentials (encrypted).
    - Body: `{ "platform": "LinkedIn", "username": "...", "password": "..." }`
- **DELETE `/credentials/{platform}`**: Remove a platform's access.
- **POST `/credentials/test/{platform}`**: Trigger a connection test task.

### 4. Job Leads (`/leads`)
- **GET `/leads`**: Fetch job leads from the central repository.
    - Query Params: `platform`, `location`, `title`, `limit`, `offset`.
- **GET `/leads/{lead_id}`**: Get detailed job description and extracted metadata.
- **POST `/leads/manual-scrape`**: (Admin/Pro) Trigger an immediate scrape for the current user's keywords.

### 5. Resumes (`/resumes`)
- **POST `/resumes/upload`**: Upload a new master resume (`.docx`).
- **GET `/resumes`**: List all uploaded and auto-generated resumes.
- **GET `/resumes/{resume_id}`**: Download a specific resume file.
- **POST `/resumes/generate-tailored`**: Manually trigger AI to generate a tailored resume for a specific `lead_id`.
    - Body: `{ "lead_id": "...", "base_resume_id": "..." }`

### 6. Applications (`/applications`)
- **POST `/applications`**: Trigger an automated application for a specific `lead_id`.
    - Body: `{ "lead_id": "...", "resume_id": "...", "platform": "LinkedIn" }`
- **GET `/applications`**: List application history for the current user.
- **GET `/applications/{app_id}/logs`**: Get real-time or historical execution logs for an application task.
- **DELETE `/applications/{app_id}`**: Cancel a pending/processing application task.

### 7. Billing & Subscriptions (`/billing`)
- **GET `/billing/plans`**: List available subscription tiers.
- **POST `/billing/subscribe`**: Initiate a Stripe checkout session.
- **POST `/billing/webhook`**: Endpoint for Stripe events (payment success, cancellation).
- **GET `/billing/invoice`**: Download recent invoices.
