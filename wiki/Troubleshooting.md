# Troubleshooting — JobAccelerator AI

This page helps you resolve common issues with JobAccelerator AI. Each section includes the problem, possible causes, and step-by-step solutions.

---

## Table of Contents

- [System Not Loading](#system-not-loading)
- [Integration Failures](#integration-failures)
- [Resume Parsing Issues](#resume-parsing-issues)
- [Payment Errors](#payment-errors)
- [Application Submission Failures](#application-submission-failures)
- [Automation Issues](#automation-issues)
- [Account Issues](#account-issues)
- [Still Need Help?](#still-need-help)

---

## System Not Loading

### Problem: The website won't load or shows a blank page

**Possible Causes:**
- Browser cache or cookies issue
- Internet connectivity problem
- Service outage

**Solutions:**

1. **Clear browser cache and cookies:**
   - Chrome: Settings → Privacy and Security → Clear Browsing Data
   - Firefox: Settings → Privacy & Security → Clear Data
   - Edge: Settings → Privacy → Clear Browsing Data
   - Select "Cached images and files" and "Cookies"
   - Click **Clear Data** and reload the page

2. **Try a different browser:**
   - If the issue persists, try Chrome, Firefox, or Edge
   - Avoid using outdated browsers (Internet Explorer is not supported)

3. **Check your internet connection:**
   - Try loading another website (e.g., google.com)
   - Restart your router if needed
   - Disable VPN temporarily — some VPNs may block access

4. **Check service status:**
   - Visit [status.jobaccelerator.ai](https://status.jobaccelerator.ai) to check for outages
   - If there's an outage, wait for the issue to be resolved

[Screenshot: Browser cache clear dialog]
> **Instruction:** Capture Chrome's "Clear Browsing Data" dialog with "Cached images and files" and "Cookies" checkboxes selected.

> **Pro Tip:** If you experience repeated loading issues, try using the platform in an **incognito/private browsing** window to rule out extension conflicts.

---

### Problem: The page loads but shows a "500 Internal Server Error"

**Possible Causes:**
- Temporary server issue
- Account-specific data error

**Solutions:**

1. **Wait and retry** — Refresh the page after 1–2 minutes
2. **Log out and log back in** — This refreshes your session
3. **Clear browser cache** — Follow steps above
4. If the error persists for more than 15 minutes, contact support with:
   - The exact error message
   - The URL where the error occurs
   - Your browser name and version
   - A screenshot of the error

---

### Problem: The dashboard is loading very slowly

**Possible Causes:**
- Large amount of application data
- Browser performance issue

**Solutions:**

1. **Reduce the date range** — Change the dashboard filter to "Last 7 days" instead of "All Time"
2. **Close unnecessary browser tabs** — Free up browser memory
3. **Disable browser extensions** — Ad blockers or privacy extensions may slow down the page
4. **Try a different browser** — Some browsers handle large datasets better

---

## Integration Failures

### Problem: LinkedIn connection fails

**Possible Causes:**
- LinkedIn security challenge triggered
- Incorrect credentials
- LinkedIn account restrictions

**Solutions:**

1. **Log in to LinkedIn manually first:**
   - Open [linkedin.com](https://linkedin.com) in your browser
   - Log in and complete any security checks (CAPTCHA, email verification)
   - Once logged in successfully, return to JobAccelerator AI

2. **Reconnect LinkedIn:**
   - Go to **Settings** → **Integrations**
   - Click the **⋮** menu next to LinkedIn → **Disconnect**
   - Wait 30 seconds
   - Click **Connect** and re-enter your credentials

3. **Check for LinkedIn restrictions:**
   - LinkedIn may restrict accounts with high activity
   - If restricted, wait 24–48 hours before reconnecting
   - Reduce your daily application limit temporarily

[Screenshot: LinkedIn reconnection flow]
> **Instruction:** Capture the Settings → Integrations page showing LinkedIn in a disconnected state with the "Connect" button visible.

> ⚠️ **Warning:** Do not attempt to reconnect more than 3 times in a row. If it keeps failing, wait 24 hours before trying again to avoid triggering LinkedIn's security systems.

---

### Problem: Indeed/Naukri connection fails

**Possible Causes:**
- Platform API changes
- Credentials changed on the platform
- Platform maintenance

**Solutions:**

1. **Verify your credentials:**
   - Log in to Indeed/Naukri directly in your browser
   - If prompted to change your password, do so
   - Then reconnect in JobAccelerator AI

2. **Disconnect and reconnect:**
   - Go to **Settings** → **Integrations**
   - Disconnect the platform, wait 30 seconds, then reconnect

3. **Check platform status:**
   - Indeed and Naukri occasionally undergo maintenance
   - Wait a few hours and try again

---

### Problem: Gmail/Outlook connection fails

**Possible Causes:**
- OAuth token expired
- Security settings blocking access
- Account permissions revoked

**Solutions:**

1. **For Gmail:**
   - Go to [myaccount.google.com/security](https://myaccount.google.com/security)
   - Check that "Less secure app access" is enabled (if applicable)
   - Or ensure you're using an **App Password** if 2FA is enabled
   - Reconnect Gmail in JobAccelerator AI

2. **For Outlook:**
   - Go to [account.microsoft.com/security](https://account.microsoft.com/security)
   - Verify that third-party app access is allowed
   - Reconnect Outlook in JobAccelerator AI

3. **Revoke and re-grant access:**
   - In your Google/Microsoft account settings, find JobAccelerator AI in connected apps
   - Revoke access, then reconnect from JobAccelerator AI

[Screenshot: Google security — connected apps]
> **Instruction:** Capture the Google Account security page showing the list of connected third-party apps, with JobAccelerator AI visible.

---

### Problem: Integration shows yellow or red status

**Status Meanings:**
- 🟢 **Green** — Connection is healthy
- 🟡 **Yellow** — Connection needs re-authentication
- 🔴 **Red** — Connection has failed

**Solutions:**

1. **Yellow (re-authentication needed):**
   - Click **Reconnect** next to the platform
   - Re-enter your credentials
   - The status should turn green

2. **Red (connection failed):**
   - Disconnect the platform completely
   - Wait 1 minute
   - Reconnect from scratch
   - If it remains red, check the [[FAQ]] for platform-specific issues

---

## Resume Parsing Issues

### Problem: Resume upload fails

**Possible Causes:**
- File too large (over 10 MB)
- Unsupported format
- File corruption

**Solutions:**

1. **Check file size:**
   - Maximum: 10 MB
   - If your file is too large, compress images or remove unnecessary pages

2. **Check file format:**
   - Supported: PDF (.pdf), DOCX (.docx)
   - Not supported: DOC (.doc), TXT (.txt), images, HTML

3. **Re-save the file:**
   - Open your resume in Word or Google Docs
   - Save as a new PDF or DOCX file
   - Try uploading the new file

[Screenshot: Resume upload error message]
> **Instruction:** Capture the upload screen showing an error message (e.g., "File too large" or "Unsupported format") with a clear indication of what went wrong.

---

### Problem: Resume parsing misses information

**Possible Causes:**
- Complex formatting (tables, columns, text boxes)
- Information in headers/footers
- Image-based content (scanned PDFs)

**Solutions:**

1. **Simplify your resume format:**
   - Use a single-column layout
   - Avoid tables, text boxes, and graphics for important information
   - Use standard fonts (Arial, Calibri, Times New Roman)

2. **Ensure text is selectable:**
   - Open your PDF and try to select/copy text
   - If you can't select text, the PDF is image-based — re-create it from a Word document

3. **Manually add missing information:**
   - Go to **Profile** → **Resume**
   - Click **Edit** on any section to add missing skills, experience, or education
   - Click **Save Changes**

4. **Use the recommended template:**
   - Download the JobAccelerator AI resume template from **Profile** → **Resume** → **Download Template**
   - Fill in your information and re-upload

[Screenshot: Manual skill editing interface]
> **Instruction:** Capture the Profile → Resume → Skills section in edit mode, showing how to add or remove skills manually.

> **Pro Tip:** The simpler your resume formatting, the better the AI can parse it. Focus on content over design for the uploaded version — the AI handles formatting for submissions.

---

### Problem: Skills are incorrectly categorized

**Possible Causes:**
- Similar skill names interpreted differently
- Industry-specific terminology not recognized

**Solutions:**

1. **Edit skills manually:**
   - Go to **Profile** → **Resume** → **Skills**
   - Remove incorrectly categorized skills
   - Re-add them under the correct category
   - Click **Save Changes**

2. **Use standard skill names:**
   - Instead of abbreviations, use full names (e.g., "JavaScript" instead of "JS")
   - Use commonly recognized skill names

---

## Payment Errors

### Problem: Payment was declined

**Possible Causes:**
- Insufficient funds
- Card expired
- Bank-side block

**Solutions:**

1. **Check your card details:**
   - Go to **Settings** → **Billing** → **Payment Method**
   - Verify the card number, expiration date, and CVV
   - If the card is expired, click **Update** and enter new card details

2. **Check your bank balance:**
   - Ensure sufficient funds are available
   - Contact your bank if you suspect a block on online transactions

3. **Try a different payment method:**
   - Add a new card in **Settings** → **Billing** → **Add Payment Method**
   - Try using a different card or PayPal

4. **Contact your bank:**
   - Some banks block international transactions by default
   - Ask your bank to whitelist transactions from JobAccelerator AI

[Screenshot: Update payment method form]
> **Instruction:** Capture the payment method update form showing card detail fields and the "Update" button.

---

### Problem: I was charged twice

**Possible Causes:**
- System error during payment processing
- Pending authorization hold (not an actual charge)

**Solutions:**

1. **Check your bank statement:**
   - Look for "pending" vs. "completed" transactions
   - Pending authorization holds usually drop off within 3–5 business days

2. **Check invoice history:**
   - Go to **Settings** → **Billing** → **Invoice History**
   - Verify if there are duplicate invoices

3. **Contact support:**
   - If you confirm a double charge, email **support@jobaccelerator.ai** with:
     - Your account email
     - Screenshots of the bank transactions
     - Invoice IDs (if available)
   - Duplicate charges are refunded within 5–7 business days

---

### Problem: Subscription not activating after payment

**Possible Causes:**
- Payment processing delay
- Browser session issue

**Solutions:**

1. **Wait 5 minutes** — Payment processing may take a moment
2. **Refresh the page** — Press F5 or click the refresh button
3. **Log out and log back in** — This refreshes your account status
4. **Check invoice history** — Confirm the payment shows as "Paid"
5. **Contact support** if the issue persists after 30 minutes

---

## Application Submission Failures

### Problem: Applications show "Failed" status

**Possible Causes:**
- Platform integration expired
- Job listing was removed
- Required application fields missing
- Rate limit exceeded

**Solutions:**

1. **Check the error message:**
   - Go to **Dashboard** → **Recent Activity**
   - Click on the failed application to see the error details

2. **Common error codes and fixes:**

| Error Code | Meaning | Fix |
|------------|---------|-----|
| `AUTH_EXPIRED` | Platform login expired | Reconnect the platform |
| `JOB_CLOSED` | Job no longer available | No action needed |
| `RATE_LIMITED` | Too many applications | Wait 24 hours |
| `PROFILE_INCOMPLETE` | Missing required fields | Complete your profile |
| `RESUME_REJECTED` | Resume format issue | Re-upload in PDF format |
| `NETWORK_ERROR` | Connection issue | Automatic retry in 1 hour |
| `CAPTCHA_REQUIRED` | Platform security challenge | Log in manually to platform |

3. **Re-enable the platform connection:**
   - Go to **Settings** → **Integrations**
   - Disconnect and reconnect the platform

[Screenshot: Failed application — error details]
> **Instruction:** Capture the application detail view showing a "Failed" status with the error code and description visible.

---

## Automation Issues

### Problem: Automation is not running

**Possible Causes:**
- Automation is paused
- Subscription expired
- No connected platforms
- Admin paused all automations

**Solutions:**

1. **Check automation status on dashboard:**
   - If it shows "Paused" → Click **Resume Automation**
   - If it shows "Inactive" → Click **Start Automation**

2. **Check your subscription:**
   - Go to **Settings** → **Billing**
   - If your subscription expired, renew it

3. **Check platform connections:**
   - Go to **Settings** → **Integrations**
   - Ensure at least one platform is connected (green status)

4. **Check for admin pause:**
   - If you see a banner "Automation temporarily paused by admin," wait for the admin to resume it

---

### Problem: Automation runs but finds no jobs

**Solutions:**

1. **Broaden your job preferences:**
   - Add more job titles
   - Add more locations or select "Remote"
   - Lower the minimum match score threshold

2. **Check the scan schedule:**
   - Jobs are scanned at specific times (default: 9:00 AM)
   - New jobs may not be available outside scanning hours

3. **Update your resume:**
   - A more detailed resume leads to better matches

---

## Account Issues

### Problem: Account suspended

**Possible Causes:**
- Payment failure (after multiple retries)
- Violation of terms of service
- Admin action

**Solutions:**

1. **Check your email:**
   - Look for a suspension notification email with the reason

2. **If payment-related:**
   - Update your payment method at the login page (a payment update link is included in the suspension email)
   - Once payment succeeds, the account is reactivated automatically

3. **If TOS violation:**
   - Contact **support@jobaccelerator.ai** to discuss and resolve the issue

---

### Problem: Not receiving emails from JobAccelerator AI

**Possible Causes:**
- Emails going to spam/junk folder
- Email address typo in account settings
- Email provider blocking the domain

**Solutions:**

1. **Check spam/junk folder:**
   - Look for emails from `noreply@jobaccelerator.ai`
   - Mark them as "Not Spam" to prevent future filtering

2. **Add to contacts:**
   - Add `noreply@jobaccelerator.ai` to your email contacts

3. **Verify your email address:**
   - Go to **Settings** → **Account** and confirm your email is correct

4. **Check email filters:**
   - Review your email filters/rules to ensure JobAccelerator AI emails aren't being auto-deleted

---

## Still Need Help?

If you couldn't resolve your issue using this guide:

1. **Search the [[FAQ]]** for additional answers
2. **Email support:** support@jobaccelerator.ai
   - Include: your account email, a description of the issue, screenshots, and any error messages
3. **In-app chat:** Click the **Help** icon in the bottom-right corner of the dashboard
4. **Community forum:** [community.jobaccelerator.ai](https://community.jobaccelerator.ai)

**Support hours:** Monday–Friday, 9:00 AM – 6:00 PM (EST)
**Response time:** Within 24 hours for email, immediate for in-app chat

---

*Return to [[Home]] | See also: [[FAQ]] | [[User Guide]] | [[Admin Guide]]*
