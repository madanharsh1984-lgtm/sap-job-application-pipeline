/**
 * API client for the JobAccelerator backend.
 * Uses fetch with JWT token stored in localStorage.
 */

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

function getToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("token");
}

async function apiFetch(path: string, options: RequestInit = {}): Promise<Response> {
  const token = getToken();
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(options.headers as Record<string, string> || {}),
  };
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const res = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers,
  });

  if (res.status === 401) {
    // Token expired or invalid — clear and redirect
    if (typeof window !== "undefined") {
      localStorage.removeItem("token");
      window.location.href = "/login";
    }
  }

  return res;
}

// ── Auth ──────────────────────────────────────────────────────────────────

export async function register(email: string, password: string) {
  const res = await apiFetch("/api/auth/register", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || "Registration failed");
  }
  return res.json();
}

export async function login(email: string, password: string) {
  const body = new URLSearchParams();
  body.append("username", email);
  body.append("password", password);

  const res = await fetch(`${API_BASE}/api/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: body.toString(),
  });

  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || "Login failed");
  }

  const data = await res.json();
  if (typeof window !== "undefined") {
    localStorage.setItem("token", data.access_token);
  }
  return data;
}

export function logout() {
  if (typeof window !== "undefined") {
    localStorage.removeItem("token");
    window.location.href = "/login";
  }
}

export async function getMe() {
  const res = await apiFetch("/api/auth/me");
  if (!res.ok) throw new Error("Failed to fetch user");
  return res.json();
}

// ── Jobs / Onboarding ─────────────────────────────────────────────────────

export async function onboard(resumeText: string) {
  const res = await apiFetch("/api/user/onboard", {
    method: "POST",
    body: JSON.stringify({ resume_text: resumeText }),
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || "Onboarding failed");
  }
  return res.json();
}

export async function getJobs() {
  const res = await apiFetch("/api/jobs");
  if (!res.ok) throw new Error("Failed to fetch jobs");
  return res.json();
}

// ── Admin ────────────────────────────────────────────────────────────────

export async function getAdminMetrics() {
  const res = await apiFetch("/api/admin/metrics");
  if (!res.ok) throw new Error("Admin access denied");
  return res.json();
}

export async function getAdminUsers() {
  const res = await apiFetch("/api/admin/users");
  if (!res.ok) throw new Error("Admin access denied");
  return res.json();
}

export async function getAdminJobs() {
  const res = await apiFetch("/api/admin/jobs");
  if (!res.ok) throw new Error("Admin access denied");
  return res.json();
}

export function isLoggedIn(): boolean {
  return !!getToken();
}
