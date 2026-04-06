# UI Wireframes: SAP Job Application SaaS Platform

This document describes the user interface structure for the commercial SaaS version.

## Page 1: Dashboard (Overview)
**Goal:** Provide a high-level summary of the user's job hunt and automation status.
- **Top Statistics Bar:**
    - Total Jobs Scraped (Current Week)
    - Total Applications Sent
    - Success Rate (Replies vs. Sends)
    - Active Automation status (Green/Red)
- **Main Chart:** Weekly application volume trends.
- **Recent Activity Feed:** Latest 5 jobs applied to and their status.
- **Alerts Box:** System notifications (e.g., "LinkedIn Login Expired", "New Lead Found").

## Page 2: Job Lead Feed (Search & Review)
**Goal:** Allow users to browse and manually trigger applications for scraped leads.
- **Filter Sidebar:** Platform (LinkedIn, Naukri, Telegram), Job Title, Location, Date Posted.
- **Job Card List:**
    - Job Title, Company, Platform Logo.
    - Status: "New", "Already Applied", "Matched".
    - Action Buttons: "View Details", "Apply Now (One-Click)", "Skip".
- **Job Detail Modal:**
    - Full Job Description.
    - Extracted Recruiter Contact (Email/Phone).
    - AI-Matched Score (User profile vs. JD).
    - Custom Resume Preview (Automatically generated for this job).

## Page 3: Profile & Credential Management
**Goal:** Securely configure the user's job search identity and platform access.
- **Credentials Section:** 
    - Card-based UI for LinkedIn, Naukri, and Gmail.
    - Status Badge: "Connected", "Connection Failed", "Not Configured".
    - "Update Connection" button: Triggers a secure modal to input/update credentials (encrypted before saving).
- **Profile Summary:**
    - High-level skills and experience (synced from resume).
    - Target Job Titles (Keywords for the scraper).
    - Preferred Locations (Remote, Onsite, Hybrid).

## Page 4: Resume Management
**Goal:** Manage base resumes and review auto-generated tailored versions.
- **Base Resume Section:** Upload/Update the master resume (`.docx`).
- **Tailored Resume History:** List of recently generated resumes per application, with download links.
- **ATS Optimizer:** A text area to paste a new JD and see how well the base resume scores before applying.

## Page 5: Application Logs & History
**Goal:** Audit trail for transparency and troubleshooting.
- **Application History Table:**
    - Date, Job Title, Company, Platform, Status (Sent/Failed), Resume Used.
- **Detailed Log View:** Click to see step-by-step automation logs (e.g., "Navigating to LinkedIn... Found Job... Uploading Resume... Success").

## Page 6: Settings & Subscription
**Goal:** Account-level settings and billing.
- **Subscription Tier:** Current plan details, upgrade options.
- **Automation Schedule:** Set preferred times for scraping and applying (e.g., "Every morning at 9 AM").
- **Notifications:** Email alerts for successful applications or failed logins.
