# Frequently Asked Questions (FAQ)

Find answers to the most common questions about JobAccelerator AI. If your question isn't listed here, check the [[Troubleshooting]] page or contact support.

---

## Table of Contents

- [General Questions](#general-questions)
- [Account & Login](#account--login)
- [Jobs & Applications](#jobs--applications)
- [Resume & Profile](#resume--profile)
- [Integrations & Connections](#integrations--connections)
- [Payments & Billing](#payments--billing)
- [Automation & Limits](#automation--limits)
- [Privacy & Security](#privacy--security)

---

## General Questions

### What is JobAccelerator AI?

JobAccelerator AI is a SaaS platform that automates your job search. It finds relevant job openings, tailors your resume, and submits applications on your behalf across multiple job platforms like LinkedIn, Indeed, and Naukri.

### Who is JobAccelerator AI for?

JobAccelerator AI is designed for:
- Job seekers who want to save time on applications
- Professionals looking for new opportunities while currently employed
- Career changers who want to maximize their exposure to relevant roles
- Anyone who finds manual job applications tedious and time-consuming

### Is JobAccelerator AI free?

JobAccelerator AI offers a **Free plan** with limited features (5 applications per day on 1 platform). Paid plans start at **$19/month** and offer more applications, multi-platform support, and advanced features. See the [[User Guide]] for plan details.

---

## Account & Login

### How do I create an account?

1. Go to [app.jobaccelerator.ai](https://app.jobaccelerator.ai)
2. Click **Sign Up**
3. Enter your name, email, and password
4. Verify your email address

See the [[Getting Started]] guide for detailed steps with screenshots.

### I forgot my password. How do I reset it?

1. Go to the login page
2. Click **Forgot Password?**
3. Enter your email address
4. Check your inbox for a reset link
5. Create a new password

> **Note:** Reset links expire after 1 hour. Request a new one if needed.

### Why can't I log in?

Common reasons:
- **Wrong password** — Try resetting your password
- **Unverified email** — Check your inbox for the verification email (including spam/junk)
- **Suspended account** — Contact support if your account has been suspended
- **Browser issues** — Clear your browser cache and cookies, then try again

### Can I change my email address?

Yes. Go to **Settings** → **Account** → **Change Email**. You'll need to verify the new email address before the change takes effect.

---

## Jobs & Applications

### Why am I not seeing any jobs?

This is one of the most common issues. Here's what to check:

1. **Check your job preferences** — Make sure your job titles and locations are not too narrow
   - Go to **Settings** → **Preferences** and review your settings
   - Try broadening your job titles (e.g., use "Manager" instead of "Senior Technical Program Manager II")
   - Add more locations or select "Remote"

2. **Check your integrations** — At least one platform must be connected
   - Go to **Settings** → **Integrations** and confirm connections are active (green dot)

3. **Check automation status** — Automation must be active
   - Look at the dashboard — automation status should show "Active"

4. **Wait for the next scan** — Jobs are scanned at scheduled intervals (typically 9:00 AM daily)
   - If you just set up your account, wait until the next scheduled scan

5. **Check your plan limits** — Free plan users see fewer matches than paid users

> **Pro Tip:** If you still don't see jobs after 24 hours, try disconnecting and reconnecting your job platforms.

### Why did my application fail?

Application failures can happen for several reasons:

| Reason | Solution |
|--------|----------|
| **Platform token expired** | Reconnect the platform in Settings → Integrations |
| **Profile incomplete** | The job requires fields you haven't filled (e.g., work authorization). Complete your profile. |
| **Rate limit exceeded** | You've reached the platform's daily application limit. Wait 24 hours. |
| **Job closed** | The job listing was removed before your application was submitted. No action needed. |
| **Resume format issue** | Upload a clean PDF or DOCX file without unusual formatting |
| **Network error** | Temporary connectivity issue. The system will retry automatically. |

### How many applications can I submit per day?

This depends on your plan:

| Plan | Applications/Day |
|------|-------------------|
| Free | 5 |
| Starter | 25 |
| Professional | 100 |
| Enterprise | Unlimited |

> **NOTE:** Assumed behavior — daily limits may also be affected by per-platform rate limits to comply with each platform's terms of service.

### Can I choose which jobs to apply to?

Yes! You have two options:

1. **Automatic mode** — The AI applies to all jobs above your minimum match score threshold
2. **Review mode** — You review and approve each application before it's submitted

Change your mode in **Settings** → **Automation** → **Application Mode**.

### Can I stop an application after it's been submitted?

No. Once an application is submitted to the job platform, it cannot be retracted through JobAccelerator AI. You would need to withdraw the application directly on the platform (e.g., LinkedIn).

---

## Resume & Profile

### What resume formats are supported?

JobAccelerator AI supports:
- **PDF** (.pdf) — Recommended
- **Microsoft Word** (.docx)
- Maximum file size: **10 MB**

> **Pro Tip:** PDF is the most reliable format. It preserves formatting and is universally accepted by employers.

### Can I have multiple resumes?

The platform stores one active resume at a time. However, the AI **automatically tailors** your resume for each job application based on the job description. You can view all versions in **Profile** → **Resume** → **Version History**.

### Why are my skills not being detected correctly?

The resume parser may not detect skills if:
- Your resume uses unusual formatting or tables
- Skills are embedded in images instead of text
- The file is scanned/image-based rather than text-based

**Solution:** Use a simple, text-based resume format. After uploading, manually edit any missing skills in **Profile** → **Resume** → **Skills**.

---

## Integrations & Connections

### Which platforms does JobAccelerator AI support?

Currently supported platforms:
- **LinkedIn** — Job search and Easy Apply
- **Indeed** — Job search and apply
- **Naukri** — Job search and auto-apply
- **Gmail** — Email-based applications and tracking
- **Outlook** — Email-based applications and tracking

### Why is my LinkedIn connection failing?

Common reasons for LinkedIn connection issues:

1. **LinkedIn security check** — LinkedIn may flag automated access. Solution:
   - Log in to LinkedIn manually in your browser
   - Complete any security challenges (CAPTCHA, verification)
   - Then reconnect in JobAccelerator AI

2. **Password changed** — If you changed your LinkedIn password, you need to reconnect

3. **Two-factor authentication** — Ensure 2FA is completed during the connection process

4. **Account restrictions** — LinkedIn may temporarily restrict accounts with high activity. Wait 24–48 hours and try again.

> ⚠️ **Warning:** LinkedIn has rate limits and usage policies. JobAccelerator AI respects these limits, but excessive manual activity combined with automation may trigger restrictions.

### Is it safe to connect my LinkedIn/Naukri account?

Yes. Your credentials are:
- Encrypted using AES-256 encryption at rest
- Transmitted over HTTPS (TLS 1.3)
- Never stored in plain text
- Never shared with third parties

---

## Payments & Billing

### What payment methods are accepted?

- Credit cards (Visa, Mastercard, American Express)
- Debit cards
- PayPal (selected regions)

> **NOTE:** Assumed behavior — specific payment methods may vary by region.

### How do I cancel my subscription?

1. Go to **Settings** → **Billing**
2. Click **Cancel Subscription**
3. Select a reason for cancellation (optional)
4. Click **Confirm Cancellation**

Your subscription remains active until the end of the current billing period. After that, your account reverts to the Free plan.

> **Note:** Cancellation does not delete your account or data. You can resubscribe at any time.

### Why was my payment declined?

Common reasons:
- **Insufficient funds** — Check your card balance
- **Card expired** — Update your payment method in Settings → Billing
- **Bank block** — Some banks block online subscriptions. Contact your bank to authorize the transaction.
- **Incorrect details** — Double-check your card number, expiration date, and CVV

If your payment fails, your automation will be paused. Update your payment method to resume.

### Can I get a refund?

Refund policy:
- Refund requests within **7 days** of purchase are processed automatically
- Requests after 7 days are reviewed on a case-by-case basis
- Contact **support@jobaccelerator.ai** for refund requests

### Where can I find my invoices?

Go to **Settings** → **Billing** → **Invoice History**. You can download any invoice as a PDF.

---

## Automation & Limits

### When does the automation run?

By default, automation runs daily at **9:00 AM** (based on your local timezone setting). You can customize the schedule in **Settings** → **Automation** → **Schedule**.

### Can I run automation multiple times per day?

Paid plans allow manual triggers:
- **Starter** — 1 scheduled run + 1 manual trigger per day
- **Professional** — 1 scheduled run + 3 manual triggers per day
- **Enterprise** — Unlimited runs

### What happens if I exceed my daily limit?

If you reach your daily application limit:
- Remaining job matches are saved for the next day
- You'll see a "Daily limit reached" notification on your dashboard
- Automation resumes the next day

### Can I pause automation temporarily?

Yes. Go to **Dashboard** and click **Pause Automation**. You can resume at any time by clicking **Resume Automation**. Your preferences and connections remain intact.

---

## Privacy & Security

### Is my data safe?

Yes. JobAccelerator AI takes security seriously:
- All data is encrypted at rest (AES-256) and in transit (TLS 1.3)
- Passwords are hashed using bcrypt
- Platform credentials are stored in encrypted vaults
- Regular security audits are conducted
- We are SOC 2 Type II compliant

> **NOTE:** Assumed behavior — compliance certifications are representative.

### Can I delete my account and all data?

Yes. Go to **Settings** → **Account** → **Delete Account**. This action:
- Removes all your personal data
- Deletes your resume and application history
- Cancels your subscription
- This action is **irreversible**

### Does JobAccelerator AI share my data with employers?

No. JobAccelerator AI only shares the information you include in your job applications (resume, cover letter, profile data). We never sell or share your personal data with third parties for marketing purposes.

---

*Still need help? Visit the [[Troubleshooting]] page or contact support at support@jobaccelerator.ai. Return to [[Home]].*
