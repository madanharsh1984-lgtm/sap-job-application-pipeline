# System Integration Test (SIT) Plan: SAP Job Application SaaS

## 1. Overview
System Integration Testing (SIT) verifies that all developed modules work together as a cohesive system. This phase focuses on data flow between the Frontend, Backend API, Database, Scrapers, AI Engine, and Payment Gateway.

## 2. Test Environment
- **Backend:** FastAPI (Local/Docker)
- **Frontend:** Next.js (Local/Docker)
- **Database:** PostgreSQL
- **Mock Services:** Mocked Stripe Webhooks and OpenAI API responses where necessary.

## 3. SIT Test Scenarios

| Scenario ID | Description | Components Involved | Expected Outcome |
| :--- | :--- | :--- | :--- |
| **SIT-01** | End-to-End User Auth | Frontend, API, Postgres, Security | User registers, hashes password, logs in, receives JWT, and accesses dashboard. |
| **SIT-02** | Automated Scraping Flow | Apify, Celery, Postgres | Trigger Celery task -> Apify Scrapes -> Leads parsed and saved in `job_leads` table. |
| **SIT-03** | AI Resume Tailoring Flow | API, OpenAI, Docx Service, S3 | User selects Job Lead + Master Resume -> AI generates tailored content -> New `.docx` created. |
| **SIT-04** | Subscription/Payment Flow | API, Stripe, Webhooks, Postgres | User triggers checkout -> Stripe sends success webhook -> User tier updated to "Pro" in DB. |
| **SIT-05** | Multi-tenant Isolation | API, Postgres | User A cannot see User B's resumes, application logs, or job leads. |

## 4. Execution Log (SIT-01 to SIT-05)
*Results will be updated in the Master Project Plan.*
