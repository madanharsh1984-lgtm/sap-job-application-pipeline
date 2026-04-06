# Beta User Onboarding Guide: JobAccelerator AI

Apply Smarter. Get Hired Faster.

Welcome to the Beta Program! This guide will help you set up your account and start your automated job search. JobAccelerator AI is a universal platform designed to handle your applications across all industries.

## 1. Getting Started
1. **Access the Portal:** Navigate to `http://localhost:3005` (Local UAT Phase).
2. **Create Your Account:** Click "Sign Up" and register with your email.
3. **Verify Email:** Check your inbox for the verification link to activate your account.

## 2. Setting Up Your Profile
1. **Upload Master Resume:** Go to the "Resumes" tab and upload your most recent `.docx` resume. This will be the base for all AI-tailored applications.
2. **Set Target Keywords:** In "Profile Settings," enter your target job titles (e.g., "Software Engineer", "Marketing Manager") and preferred locations.

## 3. Connecting Your Platforms (Secure)
To automate your applications, you must securely connect your professional accounts in the "Credentials" tab:
- **LinkedIn:** Connect for "Easy Apply" job automation.
- **Naukri:** Connect for automated applications on large job portals.
- **Gmail:** Connect to allow the AI to send tailored emails to recruiters on your behalf.
*Note: Your credentials are encrypted with AES-256 and vaulted in AWS Secrets Manager.*

## 4. Your First Automated Search
1. **Wait for Scrape:** The system runs a global scrape every morning.
2. **Review Leads:** Navigate to the "Job Feed" to see newly matched leads for your profile.
3. **Trigger AI Tailoring:** Click "Apply Now" on any lead. The AI will instantly generate a tailored resume and submit the application.
4. **Monitor Status:** Track the progress in real-time under the "Dashboard" and "Application Logs."

## 5. Providing Feedback (Beta Requirement)
As a beta user, your feedback is critical. Please report:
- **Bugs:** Any errors in login, scraping, or resume generation.
- **Improvements:** Suggestions for the dashboard or search filters.
- **Successes:** Let us know when you get a recruiter response or interview!

**Support Contact:** `beta-support@job-accelerator.ai`
