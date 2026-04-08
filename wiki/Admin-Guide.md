# Admin Guide — JobAccelerator AI

This guide is for platform administrators who manage users, monitor system health, and configure platform settings.

---

## Table of Contents

- [A. Admin Login](#a-admin-login)
- [B. Dashboard Metrics Explanation](#b-dashboard-metrics-explanation)
- [C. User Management](#c-user-management)
- [D. Payment Monitoring](#d-payment-monitoring)
- [E. Job & Application Tracking](#e-job--application-tracking)
- [F. System Control (Pause Automation)](#f-system-control-pause-automation)
- [G. Logs & Debugging](#g-logs--debugging)

---

## A. Admin Login

### Accessing the Admin Panel

1. Navigate to [admin.jobaccelerator.ai](https://admin.jobaccelerator.ai)
2. Enter your **admin email** and **admin password**
3. Complete **Two-Factor Authentication (2FA)**:
   - Enter the 6-digit code from your authenticator app (Google Authenticator, Authy, etc.)
4. Click **Log In**

[Screenshot: Admin login page]
> **Instruction:** Capture the admin login page showing the email and password fields, the 2FA input field, and the "Log In" button. The admin login page should have a distinct look (e.g., a different color or "Admin Portal" branding) compared to the user login page.

[Screenshot: Admin 2FA prompt]
> **Instruction:** Capture the two-factor authentication screen showing the 6-digit code input field and a reference to the authenticator app.

> ⚠️ **Warning:** Admin accounts require 2FA for security. If you lose access to your authenticator app, contact the system owner for a recovery code.

### Admin Roles

| Role | Permissions |
|------|-------------|
| **Super Admin** | Full access — user management, billing, system controls, logs |
| **Admin** | User management, billing view, application tracking |
| **Support Agent** | Read-only access to user data and logs for troubleshooting |

> **NOTE:** Assumed behavior — role hierarchy may vary based on your organization's configuration.

---

## B. Dashboard Metrics Explanation

After logging in, you'll see the **Admin Dashboard** with real-time metrics.

### Key Metrics

| Metric | Description |
|--------|-------------|
| **Total Users** | Total registered users (active + inactive) |
| **Active Users** | Users who logged in within the last 30 days |
| **Total Applications Today** | Sum of all job applications submitted across all users today |
| **Applications This Week** | Cumulative applications for the current week |
| **Success Rate** | Percentage of applications that received a positive response |
| **Active Automations** | Number of users with automation currently running |
| **Revenue (MRR)** | Monthly Recurring Revenue from active subscriptions |
| **Churn Rate** | Percentage of users who cancelled in the last 30 days |

[Screenshot: Admin dashboard — full metrics view]
> **Instruction:** Capture the complete admin dashboard showing all key metrics as cards or tiles at the top. Include sample data (e.g., Total Users: 1,245; Active Users: 892; MRR: $18,450). Show graphs/charts below the metrics.

### Dashboard Charts

- **User Growth** — Line chart showing new registrations over time
- **Applications Trend** — Bar chart of daily applications for the past 30 days
- **Revenue Trend** — Line chart of MRR over the past 12 months
- **Platform Distribution** — Pie chart showing which job platforms are most used

[Screenshot: Admin dashboard charts]
> **Instruction:** Capture the charts section of the admin dashboard showing at least the User Growth and Applications Trend charts with sample data.

> **Pro Tip:** Use the **date range picker** at the top-right of the dashboard to change the reporting period. Export charts as images by clicking the **Download** icon on each chart.

---

## C. User Management

### Viewing All Users

1. Click **Users** in the left sidebar menu
2. The user list shows all registered users with:
   - Name and email
   - Subscription plan
   - Account status (Active, Suspended, Deactivated)
   - Registration date
   - Last login date
   - Total applications submitted

[Screenshot: User management — user list table]
> **Instruction:** Capture the user list page showing a table with 5–10 users. Include column headers (Name, Email, Plan, Status, Registered, Last Login, Applications). Show different statuses for different users.

### Searching and Filtering Users

1. Use the **Search** bar to find users by name or email
2. Use the **Filter** dropdown to filter by:
   - Subscription plan (Free, Starter, Professional, Enterprise)
   - Account status (Active, Suspended, Deactivated)
   - Registration date range
3. Click **Apply Filters**

[Screenshot: User list with active filters]
> **Instruction:** Capture the user list with the filter panel open, showing filters applied (e.g., Plan: Professional, Status: Active). Show the filtered results.

### Managing Individual Users

1. Click on a user's row to open their **User Detail** page
2. Available actions:
   - **View Profile** — See user's resume, preferences, and integration status
   - **View Applications** — See all applications submitted by this user
   - **Suspend Account** — Temporarily disable the user's account
   - **Reactivate Account** — Re-enable a suspended account
   - **Reset Password** — Send a password reset email to the user
   - **Delete Account** — Permanently remove the user and all their data

[Screenshot: User detail page with action buttons]
> **Instruction:** Capture the user detail page showing user info (name, email, plan, status) and action buttons (Suspend, Reset Password, Delete). Show the user's subscription plan and application count.

> ⚠️ **Warning:** Deleting a user account is **irreversible**. All data including applications, resume, and payment history will be permanently removed. A confirmation dialog will appear before deletion.

### Suspending a User

1. Open the user's detail page
2. Click **Suspend Account**
3. Enter a reason for suspension
4. Click **Confirm Suspension**
5. The user will be logged out and unable to log in until reactivated

[Screenshot: Suspend account confirmation dialog]
> **Instruction:** Capture the suspension confirmation dialog showing the reason input field and "Confirm Suspension" button.

---

## D. Payment Monitoring

### Viewing Revenue

1. Click **Billing** in the left sidebar menu
2. The billing dashboard shows:
   - **MRR** (Monthly Recurring Revenue)
   - **Total Revenue** (all time)
   - **Active Subscriptions** by plan
   - **Failed Payments** requiring attention
   - **Upcoming Renewals** in the next 7 days

[Screenshot: Admin billing dashboard]
> **Instruction:** Capture the admin billing dashboard showing revenue summary cards (MRR, Total Revenue, Active Subscriptions, Failed Payments) and a revenue chart.

### Managing Failed Payments

1. On the Billing page, click the **Failed Payments** section
2. View the list of users with failed payments:
   - User name and email
   - Plan and amount
   - Failure reason (e.g., "Insufficient funds," "Card expired")
   - Failure date
3. Actions:
   - Click **Retry Payment** to attempt the charge again
   - Click **Notify User** to send a payment failure email
   - Click **Suspend** to pause the user's account until payment is resolved

[Screenshot: Failed payments list]
> **Instruction:** Capture the failed payments table showing 2–3 entries with user names, amounts, failure reasons, and action buttons (Retry, Notify, Suspend).

### Viewing Invoices

1. Click **Billing** → **All Invoices**
2. Browse or search invoices by:
   - User name or email
   - Date range
   - Amount range
   - Payment status (Paid, Failed, Refunded)
3. Click **Download** to export an invoice as PDF

[Screenshot: Invoice list with filters]
> **Instruction:** Capture the invoices table showing invoices with statuses (Paid with green badge, Failed with red badge). Include the search/filter bar and "Download" button.

> **Pro Tip:** Set up **automated payment retry** in Settings → Billing → Retry Policy to automatically retry failed payments after 3, 7, and 14 days.

---

## E. Job & Application Tracking

### Viewing All Applications

1. Click **Applications** in the left sidebar menu
2. The applications list shows all submissions across all users:
   - Application ID
   - User name
   - Job title and company
   - Platform (LinkedIn, Indeed, Naukri)
   - Status (Submitted, Viewed, Response Received, Rejected)
   - Submission date

[Screenshot: Admin applications list]
> **Instruction:** Capture the applications table showing 5–10 entries with different statuses (Submitted, Viewed, Rejected) indicated by colored badges. Include the filter bar.

### Application Status Definitions

| Status | Meaning |
|--------|---------|
| **Submitted** | Application was successfully sent to the employer |
| **Viewed** | Employer opened/viewed the application |
| **Response Received** | Employer sent a reply (interview, follow-up, etc.) |
| **Rejected** | Application was declined |
| **Failed** | Application submission encountered an error |

### Tracking Job Sources

1. Click **Applications** → **By Source**
2. View application distribution across platforms:
   - Number of applications per platform
   - Success rate per platform
   - Average response time per platform

[Screenshot: Applications by source — platform breakdown]
> **Instruction:** Capture the platform breakdown view showing a chart or table with per-platform statistics (LinkedIn: 450 apps, 12% response rate; Indeed: 200 apps, 8% response rate, etc.).

---

## F. System Control (Pause Automation)

### Pausing All Automation

In case of issues, you can pause automation for all users:

1. Click **System** in the left sidebar menu
2. Click **Automation Control**
3. Click the **Pause All** button
4. Enter a reason for pausing (e.g., "Platform maintenance," "Rate limit exceeded")
5. Click **Confirm Pause**
6. All active automations will stop immediately
7. Users will see a banner: "Automation temporarily paused by admin"

[Screenshot: System — Automation Control page]
> **Instruction:** Capture the automation control page showing the "Pause All" button, the current automation status (Active), and a count of running automations. Include the reason input field.

[Screenshot: User dashboard with "Automation paused by admin" banner]
> **Instruction:** Capture a user's dashboard view showing the admin-paused banner at the top of the page.

> ⚠️ **Warning:** Pausing automation affects **all users**. Only pause in case of system-wide issues. For individual user issues, suspend the specific user's automation from their detail page.

### Resuming Automation

1. On the **Automation Control** page, click **Resume All**
2. Confirm the action
3. All previously active automations will restart

### Pausing Automation for a Single User

1. Go to **Users** → Select the user
2. Click **Pause Automation** on their detail page
3. Enter a reason
4. Click **Confirm**

[Screenshot: Single user automation pause]
> **Instruction:** Capture the user detail page showing the "Pause Automation" button and the automation status for that specific user.

### Rate Limit Management

1. Go to **System** → **Rate Limits**
2. View and configure rate limits per platform:
   - LinkedIn: Max applications per day per user
   - Indeed: Max applications per day per user
   - Naukri: Max applications per day per user
3. Adjust limits based on platform guidelines to avoid account restrictions

[Screenshot: Rate limit configuration]
> **Instruction:** Capture the rate limits page showing configurable limits per platform with input fields and current values.

---

## G. Logs & Debugging

### Viewing System Logs

1. Click **System** in the left sidebar menu
2. Click **Logs**
3. View logs categorized by:
   - **Application Logs** — Detailed log of each application submission
   - **Error Logs** — Failed operations and error messages
   - **Audit Logs** — Admin actions (user suspension, system pauses, etc.)
   - **Integration Logs** — Platform connection events and API calls

[Screenshot: System logs page]
> **Instruction:** Capture the logs page showing log category tabs (Application, Error, Audit, Integration) with the Application Logs tab selected. Show 5–10 log entries with timestamps, severity levels, and messages.

### Filtering Logs

1. Use the **Log Level** filter:
   - **INFO** — Normal operations
   - **WARNING** — Non-critical issues
   - **ERROR** — Failed operations requiring attention
   - **CRITICAL** — System-level failures
2. Use the **Date Range** picker to narrow results
3. Use the **Search** bar to find specific log entries by keyword
4. Click **Export** to download logs as CSV

[Screenshot: Logs with filters applied]
> **Instruction:** Capture the logs page with filters active (e.g., Level: ERROR, Date: Last 24 hours). Show filtered log entries with red/orange severity indicators.

### Debugging Common Issues

#### Application Submission Failures

1. Go to **Logs** → **Error Logs**
2. Filter by keyword: "application" or "submit"
3. Check for common errors:
   - `AUTH_EXPIRED` — User's platform token expired → Notify user to reconnect
   - `RATE_LIMITED` — Platform rate limit exceeded → Reduce daily limits
   - `PROFILE_INCOMPLETE` — Required fields missing → Check user's profile
   - `NETWORK_ERROR` — Connectivity issue → Check system health

#### Integration Connection Issues

1. Go to **Logs** → **Integration Logs**
2. Filter by platform name (e.g., "LinkedIn")
3. Common issues:
   - `OAUTH_REVOKED` — User revoked access → Ask user to reconnect
   - `API_CHANGED` — Platform API updated → Check for system updates
   - `TIMEOUT` — Connection timed out → Check network and retry

[Screenshot: Error log detail view]
> **Instruction:** Capture a detailed error log entry showing the full error message, stack trace (if available), user ID, timestamp, and related metadata.

### System Health Dashboard

1. Go to **System** → **Health**
2. View real-time system status:
   - **API Server** — Status and response time
   - **Database** — Connection status and query performance
   - **Redis / Cache** — Cache hit rate and memory usage
   - **Worker Queue** — Pending jobs and processing rate
   - **Browser Service** — Automation engine status

[Screenshot: System health dashboard]
> **Instruction:** Capture the health dashboard showing all system components with green (healthy), yellow (degraded), or red (down) status indicators. Include response time metrics.

> **Pro Tip:** Set up alerts in **System** → **Alerts** to receive email or Slack notifications when system components become unhealthy. Configure thresholds for response time, error rate, and queue depth.

---

## Admin Best Practices

1. **Check the dashboard daily** — Review key metrics and failed payments
2. **Monitor error logs** — Address recurring errors before they affect users
3. **Review rate limits weekly** — Adjust based on platform changes
4. **Respond to failed payments promptly** — Revenue depends on it
5. **Use audit logs** — Track all admin actions for accountability
6. **Set up alerts** — Don't rely on manual checks for critical issues
7. **Rotate admin credentials quarterly** — Change passwords and update 2FA

---

*Return to [[Home]] | See also: [[User Guide]] | [[Troubleshooting]]*
