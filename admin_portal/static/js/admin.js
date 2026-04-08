// =============================================================================
// admin.js — Admin Portal Frontend Logic (ADMIN_PORTAL_v1)
// =============================================================================

const API_BASE = '/admin';

// ── AUTH ──────────────────────────────────────────────────────────────────────

function getToken() {
    return localStorage.getItem('admin_token');
}

function setToken(token) {
    localStorage.setItem('admin_token', token);
}

function clearToken() {
    localStorage.removeItem('admin_token');
}

function requireAuth() {
    if (!getToken()) {
        window.location.href = '/';
        return false;
    }
    return true;
}

function logout() {
    clearToken();
    window.location.href = '/';
}

// ── API HELPERS ──────────────────────────────────────────────────────────────

async function apiGet(path) {
    const resp = await fetch(`${API_BASE}${path}`, {
        headers: { 'Authorization': `Bearer ${getToken()}` }
    });
    if (resp.status === 401 || resp.status === 403) {
        clearToken();
        window.location.href = '/';
        return null;
    }
    return resp.json();
}

async function apiPost(path, data) {
    const resp = await fetch(`${API_BASE}${path}`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${getToken()}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });
    if (resp.status === 401 || resp.status === 403) {
        clearToken();
        window.location.href = '/';
        return null;
    }
    return resp.json();
}

async function apiPut(path, data) {
    const resp = await fetch(`${API_BASE}${path}`, {
        method: 'PUT',
        headers: {
            'Authorization': `Bearer ${getToken()}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });
    return resp.json();
}

// ── UI HELPERS ───────────────────────────────────────────────────────────────

function showAlert(id, message, type) {
    const el = document.getElementById(id);
    if (!el) return;
    el.className = `alert alert-${type}`;
    el.textContent = message;
    el.style.display = 'block';
    setTimeout(() => { el.style.display = 'none'; }, 5000);
}

function statusBadge(status) {
    const map = {
        'success': 'success',
        'active': 'success',
        'sent': 'success',
        'applied': 'success',
        'failed': 'danger',
        'error': 'danger',
        'inactive': 'secondary',
        'pending': 'warning',
        'refunded': 'info',
        'true': 'success',
        'false': 'secondary'
    };
    const cls = map[String(status).toLowerCase()] || 'secondary';
    return `<span class="badge badge-${cls}">${status}</span>`;
}

function formatDate(iso) {
    if (!iso) return '—';
    const d = new Date(iso);
    return d.toLocaleDateString() + ' ' + d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

function renderPagination(container, page, pages, callback) {
    const el = document.getElementById(container);
    if (!el) return;
    let html = '';
    html += `<button ${page <= 1 ? 'disabled' : ''} onclick="${callback}(${page - 1})">← Prev</button>`;
    html += `<span>Page ${page} of ${pages}</span>`;
    html += `<button ${page >= pages ? 'disabled' : ''} onclick="${callback}(${page + 1})">Next →</button>`;
    el.innerHTML = html;
}

// ── LOGIN ────────────────────────────────────────────────────────────────────

async function handleLogin(e) {
    e.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    try {
        const resp = await fetch(`${API_BASE}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });
        const data = await resp.json();
        if (resp.ok) {
            setToken(data.token);
            window.location.href = '/dashboard';
        } else {
            showAlert('login-alert', data.error || 'Login failed', 'danger');
        }
    } catch {
        showAlert('login-alert', 'Connection error', 'danger');
    }
}

async function handleSetup(e) {
    e.preventDefault();
    const name = document.getElementById('setup-name').value;
    const email = document.getElementById('setup-email').value;
    const password = document.getElementById('setup-password').value;

    try {
        const resp = await fetch(`${API_BASE}/auth/setup`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, email, password })
        });
        const data = await resp.json();
        if (resp.ok) {
            setToken(data.token);
            window.location.href = '/dashboard';
        } else {
            showAlert('setup-alert', data.error || 'Setup failed', 'danger');
        }
    } catch {
        showAlert('setup-alert', 'Connection error', 'danger');
    }
}

// ── DASHBOARD ────────────────────────────────────────────────────────────────

async function loadDashboard() {
    if (!requireAuth()) return;
    const data = await apiGet('/dashboard-metrics');
    if (!data) return;

    const fields = {
        'total-users': data.total_users,
        'active-daily': data.active_users_daily,
        'active-weekly': data.active_users_weekly,
        'total-jobs': data.total_jobs_discovered,
        'total-apps': data.total_applications_sent,
        'failed-apps': data.failed_applications,
        'conversion': data.conversion_rate + '%',
        'revenue-daily': '₹' + (data.revenue_daily || 0).toLocaleString(),
        'revenue-monthly': '₹' + (data.revenue_monthly || 0).toLocaleString()
    };

    for (const [id, val] of Object.entries(fields)) {
        const el = document.getElementById(id);
        if (el) el.textContent = val;
    }
}

// ── USERS ────────────────────────────────────────────────────────────────────

async function loadUsers(page = 1) {
    if (!requireAuth()) return;
    const search = document.getElementById('user-search')?.value || '';
    const status = document.getElementById('user-status')?.value || '';
    const data = await apiGet(`/users?page=${page}&search=${encodeURIComponent(search)}&status=${status}`);
    if (!data) return;

    const tbody = document.getElementById('users-tbody');
    if (!tbody) return;

    if (data.users.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="empty-state"><p>No users found</p></td></tr>';
    } else {
        tbody.innerHTML = data.users.map(u => `
            <tr>
                <td>${u.id}</td>
                <td><strong>${u.name}</strong><br><small>${u.email}</small></td>
                <td>${u.role}</td>
                <td>${statusBadge(u.is_active ? 'Active' : 'Inactive')}</td>
                <td>${u.integrations_count}</td>
                <td>${u.applications_count}</td>
                <td>
                    <button class="btn btn-sm btn-outline" onclick="viewUser(${u.id})">View</button>
                    <button class="btn btn-sm ${u.is_active ? 'btn-danger' : 'btn-success'}"
                        onclick="toggleUser(${u.id}, '${u.is_active ? 'deactivate' : 'activate'}')">
                        ${u.is_active ? 'Disable' : 'Enable'}
                    </button>
                </td>
            </tr>
        `).join('');
    }
    renderPagination('users-pagination', data.page, data.pages, 'loadUsers');
}

async function viewUser(userId) {
    const data = await apiGet(`/user/${userId}`);
    if (!data) return;

    let details = `
        <h3>${data.name} (${data.email})</h3>
        <p><strong>Role:</strong> ${data.role} | <strong>Status:</strong> ${data.is_active ? 'Active' : 'Inactive'} | <strong>Paused:</strong> ${data.is_paused ? 'Yes' : 'No'}</p>
        <p><strong>Daily Limit:</strong> ${data.daily_application_limit} | <strong>Jobs Discovered:</strong> ${data.total_jobs_discovered} | <strong>Applications Sent:</strong> ${data.total_applications_sent}</p>
        <p><strong>Keywords:</strong> ${data.keywords?.join(', ') || 'None'}</p>
        <h4 style="margin-top:16px">Integrations</h4>
        <ul>${data.integrations.map(i => `<li>${i.platform}: ${statusBadge(i.status)}</li>`).join('') || '<li>None</li>'}</ul>
        <h4 style="margin-top:16px">Resumes</h4>
        <ul>${data.resumes.map(r => `<li>${r.filename} ${r.is_tailored ? '(Tailored)' : ''}</li>`).join('') || '<li>None</li>'}</ul>
        <div style="margin-top:16px">
            <button class="btn btn-sm btn-warning" onclick="resetIntegrations(${userId})">Reset Integrations</button>
            <button class="btn btn-sm btn-outline" onclick="setUserLimit(${userId})">Set Daily Limit</button>
            <button class="btn btn-sm btn-outline" onclick="pauseUser(${userId}, ${!data.is_paused})">${data.is_paused ? 'Resume' : 'Pause'} Automation</button>
        </div>
    `;
    document.getElementById('user-detail').innerHTML = details;
    document.getElementById('user-detail').style.display = 'block';
}

async function toggleUser(userId, action) {
    await apiPost('/user/disable', { user_id: userId, action });
    showAlert('users-alert', `User ${action}d successfully`, 'success');
    loadUsers();
}

async function resetIntegrations(userId) {
    await apiPost('/user/reset-integrations', { user_id: userId });
    showAlert('users-alert', 'Integrations reset successfully', 'success');
    viewUser(userId);
}

async function setUserLimit(userId) {
    const limit = prompt('Enter daily application limit:', '50');
    if (limit === null) return;
    await apiPost('/user/set-limit', { user_id: userId, limit: parseInt(limit, 10) });
    showAlert('users-alert', 'Limit updated', 'success');
    viewUser(userId);
}

async function pauseUser(userId, paused) {
    await apiPost('/system/pause', { scope: 'user', user_id: userId, paused });
    showAlert('users-alert', `User automation ${paused ? 'paused' : 'resumed'}`, 'success');
    viewUser(userId);
}

// ── PAYMENTS ─────────────────────────────────────────────────────────────────

async function loadPayments(page = 1) {
    if (!requireAuth()) return;
    const status = document.getElementById('payment-status')?.value || '';
    const data = await apiGet(`/payments?page=${page}&status=${status}`);
    if (!data) return;

    const tbody = document.getElementById('payments-tbody');
    if (!tbody) return;

    if (data.payments.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="empty-state"><p>No payments found</p></td></tr>';
    } else {
        tbody.innerHTML = data.payments.map(p => `
            <tr class="${p.is_suspicious ? 'suspicious' : ''}">
                <td>${p.id}</td>
                <td>${p.user_id}</td>
                <td>₹${p.amount.toLocaleString()}</td>
                <td>${statusBadge(p.status)}</td>
                <td>${p.subscription_plan || '—'}</td>
                <td>${formatDate(p.created_at)}</td>
                <td>
                    <button class="btn btn-sm btn-warning" onclick="refundPayment(${p.id})" ${p.status === 'refunded' ? 'disabled' : ''}>Refund</button>
                    <button class="btn btn-sm btn-outline" onclick="flagPayment(${p.id})">${p.is_suspicious ? 'Unflag' : 'Flag'}</button>
                </td>
            </tr>
        `).join('');
    }
    renderPagination('payments-pagination', data.page, data.pages, 'loadPayments');
}

async function refundPayment(paymentId) {
    if (!confirm('Confirm refund?')) return;
    await apiPost('/payment/refund', { payment_id: paymentId });
    showAlert('payments-alert', 'Payment refunded', 'success');
    loadPayments();
}

async function flagPayment(paymentId) {
    await apiPost('/payment/flag', { payment_id: paymentId });
    showAlert('payments-alert', 'Payment flag toggled', 'warning');
    loadPayments();
}

// ── JOBS & APPLICATIONS ──────────────────────────────────────────────────────

async function loadJobs(page = 1) {
    if (!requireAuth()) return;
    const platform = document.getElementById('job-platform')?.value || '';
    const data = await apiGet(`/jobs?page=${page}&platform=${platform}`);
    if (!data) return;

    const tbody = document.getElementById('jobs-tbody');
    if (!tbody) return;

    if (data.jobs.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" class="empty-state"><p>No jobs found</p></td></tr>';
    } else {
        tbody.innerHTML = data.jobs.map(j => `
            <tr>
                <td>${j.id}</td>
                <td><strong>${j.title}</strong><br><small>${j.company || '—'}</small></td>
                <td>${j.platform}</td>
                <td>${j.location || '—'}</td>
                <td>${j.applications_count}</td>
                <td>${formatDate(j.scraped_at)}</td>
            </tr>
        `).join('');
    }
    renderPagination('jobs-pagination', data.page, data.pages, 'loadJobs');

    // Platform breakdown
    if (data.platform_breakdown) {
        const bk = document.getElementById('job-breakdown');
        if (bk) {
            bk.innerHTML = Object.entries(data.platform_breakdown)
                .map(([p, c]) => `<span class="badge badge-info" style="margin-right:8px">${p}: ${c}</span>`)
                .join('');
        }
    }
}

async function loadApplications(page = 1) {
    if (!requireAuth()) return;
    const status = document.getElementById('app-status')?.value || '';
    const platform = document.getElementById('app-platform')?.value || '';
    const data = await apiGet(`/applications?page=${page}&status=${status}&platform=${platform}`);
    if (!data) return;

    const tbody = document.getElementById('apps-tbody');
    if (!tbody) return;

    if (data.applications.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" class="empty-state"><p>No applications found</p></td></tr>';
    } else {
        tbody.innerHTML = data.applications.map(a => `
            <tr>
                <td>${a.id}</td>
                <td>${a.user_id}</td>
                <td>${a.platform}</td>
                <td>${statusBadge(a.status)}</td>
                <td>${a.failure_reason || '—'}</td>
                <td>${formatDate(a.applied_at)}</td>
            </tr>
        `).join('');
    }
    renderPagination('apps-pagination', data.page, data.pages, 'loadApplications');

    // Failure breakdown
    if (data.failure_breakdown) {
        const fb = document.getElementById('failure-breakdown');
        if (fb) {
            fb.innerHTML = Object.entries(data.failure_breakdown)
                .map(([r, c]) => `<span class="badge badge-danger" style="margin-right:8px">${r}: ${c}</span>`)
                .join('');
        }
    }
}

// ── SYSTEM LOGS ──────────────────────────────────────────────────────────────

async function loadSystemLogs(page = 1) {
    if (!requireAuth()) return;
    const level = document.getElementById('log-level')?.value || '';
    const source = document.getElementById('log-source')?.value || '';
    const data = await apiGet(`/system-logs?page=${page}&level=${level}&source=${source}`);
    if (!data) return;

    const tbody = document.getElementById('logs-tbody');
    if (!tbody) return;

    if (data.logs.length === 0) {
        tbody.innerHTML = '<tr><td colspan="4" class="empty-state"><p>No logs found</p></td></tr>';
    } else {
        tbody.innerHTML = data.logs.map(l => `
            <tr>
                <td><span class="log-${l.level}">${l.level.toUpperCase()}</span></td>
                <td>${l.source}</td>
                <td>${l.message}</td>
                <td>${formatDate(l.created_at)}</td>
            </tr>
        `).join('');
    }
    renderPagination('logs-pagination', data.page, data.pages, 'loadSystemLogs');
}

// ── SETTINGS ─────────────────────────────────────────────────────────────────

async function loadSettings() {
    if (!requireAuth()) return;
    const data = await apiGet('/settings');
    if (!data) return;

    const s = data.settings;
    const paused = document.getElementById('setting-global-pause');
    const limit = document.getElementById('setting-daily-limit');
    const freq = document.getElementById('setting-scraping-freq');

    if (paused) paused.checked = s.global_automation_paused === 'true';
    if (limit) limit.value = s.default_daily_application_limit || '50';
    if (freq) freq.value = s.scraping_frequency_minutes || '60';
}

async function saveSettings() {
    const settings = {
        global_automation_paused: document.getElementById('setting-global-pause')?.checked ? 'true' : 'false',
        default_daily_application_limit: document.getElementById('setting-daily-limit')?.value || '50',
        scraping_frequency_minutes: document.getElementById('setting-scraping-freq')?.value || '60'
    };

    await apiPut('/settings', settings);
    showAlert('settings-alert', 'Settings saved successfully', 'success');
}

async function pauseAllAutomation() {
    const paused = document.getElementById('setting-global-pause')?.checked;
    await apiPost('/system/pause', { scope: 'global', paused });
    showAlert('settings-alert', `Automation ${paused ? 'paused' : 'resumed'}`, paused ? 'warning' : 'success');
}
