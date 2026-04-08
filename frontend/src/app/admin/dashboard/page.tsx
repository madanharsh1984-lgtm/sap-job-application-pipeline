"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import NavBar from "@/components/NavBar";
import { getMe, getAdminMetrics, isLoggedIn } from "@/lib/api";

interface Metrics {
  total_users: number;
  total_jobs: number;
  total_keyword_sets: number;
  total_resumes: number;
}

export default function AdminDashboardPage() {
  const router = useRouter();
  const [metrics, setMetrics] = useState<Metrics | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!isLoggedIn()) {
      router.replace("/admin/login");
      return;
    }

    async function load() {
      try {
        const me = await getMe();
        if (me.role !== "admin") {
          router.replace("/dashboard");
          return;
        }
        const data = await getAdminMetrics();
        setMetrics(data);
      } catch {
        setError("Failed to load admin dashboard");
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [router]);

  if (loading) return <div className="loading">Loading admin dashboard...</div>;
  if (error) return <div className="page-container"><div className="error-msg">{error}</div></div>;

  return (
    <>
      <NavBar isAdmin />
      <div className="page-container">
        <h1>Admin Dashboard</h1>
        <p style={{ color: "var(--text-muted)", marginBottom: "1.5rem" }}>
          System overview and key metrics
        </p>

        <div className="metrics-grid">
          <div className="metric-card">
            <div className="metric-value">{metrics?.total_users ?? 0}</div>
            <div className="metric-label">Total Users</div>
          </div>
          <div className="metric-card">
            <div className="metric-value">{metrics?.total_jobs ?? 0}</div>
            <div className="metric-label">Total Jobs</div>
          </div>
          <div className="metric-card">
            <div className="metric-value">{metrics?.total_keyword_sets ?? 0}</div>
            <div className="metric-label">Keyword Sets</div>
          </div>
          <div className="metric-card">
            <div className="metric-value">{metrics?.total_resumes ?? 0}</div>
            <div className="metric-label">Resumes Uploaded</div>
          </div>
        </div>
      </div>
    </>
  );
}
