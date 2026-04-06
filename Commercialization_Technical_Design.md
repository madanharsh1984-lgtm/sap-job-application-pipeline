# System Architecture & Database Schema: JobAccelerator AI

Apply Smarter. Get Hired Faster.

## 1. High-Level System Architecture

JobAccelerator AI is a universal, multi-tenant SaaS platform designed to automate the job application lifecycle for candidates across all industries (IT, Non-IT, Finance, Marketing, etc.). To support 10,000+ users, we must decouple the user interface from the heavy automation tasks (scraping, resume generation, and emailing).

### Architecture Components:
1. **Frontend (Web Application):** 
   - **Tech:** Next.js (React), Tailwind CSS.
   - **Role:** User dashboard, profile settings, real-time job feed, application logs.
2. **Backend API (Central Controller):**
   - **Tech:** Python (FastAPI).
   - **Role:** Handles authentication, API requests from the frontend, and dispatches heavy tasks to the worker queue.
3. **Asynchronous Task Queue:**
   - **Tech:** Celery with Redis (or RabbitMQ).
   - **Role:** Essential for scaling. Instead of a script running one-by-one, workers process thousands of scraping/emailing tasks in parallel.
4. **Scraping Infrastructure:**
   - **Tech:** Apify (Enterprise) + Proxy Rotation (BrightData).
   - **Role:** Centralized scraping using a master token, avoiding individual user tokens.
5. **Credential Security:**
   - **Tech:** AWS Secrets Manager or HashiCorp Vault.
   - **Role:** Every user's LinkedIn/Naukri/Gmail password is encrypted at rest. The Backend retrieves them only when needed for an active task.
6. **Object Storage:**
   - **Tech:** AWS S3.
   - **Role:** Stores all user-uploaded and AI-generated `.docx` resumes.

---

## 2. Database Schema (PostgreSQL - Multi-tenant)

This relational schema ensures data integrity and strict isolation between users.

### Table: `users`
| Column | Type | Description |
| :--- | :--- | :--- |
| `user_id` | UUID (PK) | Unique internal ID. |
| `email` | String (Unique) | User login email. |
| `password_hash` | String | Bcrypt hash of the portal password. |
| `subscription_tier` | Enum | Free, Beta, Pro, Enterprise. |
| `created_at` | Timestamp | Registration date. |

### Table: `user_credentials` (Encrypted Store)
| Column | Type | Description |
| :--- | :--- | :--- |
| `id` | UUID (PK) | |
| `user_id` | UUID (FK) | Reference to `users`. |
| `platform` | Enum | 'LinkedIn', 'Naukri', 'Gmail'. |
| `secret_path` | String | Pointer to the secret in AWS Secrets Manager. |
| `status` | Enum | 'Active', 'Expired', 'Invalid'. |

### Table: `job_leads` (Central Repository)
| Column | Type | Description |
| :--- | :--- | :--- |
| `lead_id` | UUID (PK) | |
| `platform` | Enum | LinkedIn, Naukri, Telegram, etc. |
| `job_title` | String | |
| `company` | String | |
| `location` | String | |
| `raw_text` | Text | Full job description. |
| `recruiter_email` | String | Extracted email address. |
| `scraped_at` | Timestamp | |

### Table: `resumes`
| Column | Type | Description |
| :--- | :--- | :--- |
| `resume_id` | UUID (PK) | |
| `user_id` | UUID (FK) | Reference to `users`. |
| `file_name` | String | |
| `s3_path` | String | Path to the `.docx` in AWS S3. |
| `is_base` | Boolean | True if this is the default master resume. |

### Table: `applications`
| Column | Type | Description |
| :--- | :--- | :--- |
| `app_id` | UUID (PK) | |
| `user_id` | UUID (FK) | |
| `lead_id` | UUID (FK) | |
| `resume_id` | UUID (FK) | The specific version used for this app. |
| `status` | Enum | 'Pending', 'Processing', 'Sent', 'Failed'. |
| `log` | Text | Any error messages (e.g., "LinkedIn Login Blocked"). |
| `sent_at` | Timestamp | |

---

## 3. Data Flow Overview

1. **User Login:** Authenticates against the `users` table.
2. **Setup:** User uploads a base resume (stored in S3) and provides credentials (stored in Secrets Manager).
3. **Scraping:** A scheduled Celery task runs Apify (via master token) and populates the `job_leads` table.
4. **Matching:** A background worker matches `users` profiles with `job_leads`.
5. **Execution:** 
   - A task is created in the `applications` table.
   - A worker fetches the `secret_path`, generates a tailored resume, and calls the `linkedin_easy_apply` or `send_emails` logic.
   - Status is updated in real-time on the user’s dashboard.
