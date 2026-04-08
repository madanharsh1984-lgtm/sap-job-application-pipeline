"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import NavBar from "@/components/NavBar";
import { getMe, getJobs, isLoggedIn } from "@/lib/api";

interface Job {
  id: number;
  title: string;
  company: string | null;
  location: string | null;
  source: string | null;
  created_at: string;
}

export default function DashboardPage() {
  const router = useRouter();
  const [user, setUser] = useState<{ email: string; role: string } | null>(null);
  const [jobCount, setJobCount] = useState(0);
  const [jobs, setJobs] = useState<Job[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!isLoggedIn()) {
      router.replace("/login");
      return;
    }

    async function load() {
      try {
        const [me, jobData] = await Promise.all([getMe(), getJobs()]);
        setUser(me);
        setJobCount(jobData.total);
        setJobs(jobData.jobs.slice(0, 10));
      } catch {
        router.replace("/login");
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [router]);

  if (loading) return <div className="loading">Loading dashboard...</div>;

  return (
    <>
      <NavBar />
      <div className="page-container">
        <h1>Dashboard</h1>
        <p style={{ color: "var(--text-muted)", marginBottom: "1.5rem" }}>
          Welcome back, {user?.email}
        </p>

        <div className="metrics-grid">
          <div className="metric-card">
            <div className="metric-value">{jobCount}</div>
            <div className="metric-label">Qualified Jobs</div>
          </div>
          <div className="metric-card">
            <div className="metric-value">{user?.role === "admin" ? "Admin" : "User"}</div>
            <div className="metric-label">Account Type</div>
          </div>
        </div>

        {jobCount > 0 && (
          <div className="card">
            <h2 style={{ marginBottom: "0.5rem" }}>
              You are eligible for {jobCount} jobs
            </h2>
            <p style={{ color: "var(--text-muted)", marginBottom: "1rem" }}>
              Showing latest {Math.min(10, jobs.length)} results
            </p>
            <table>
              <thead>
                <tr>
                  <th>Title</th>
                  <th>Company</th>
                  <th>Location</th>
                  <th>Source</th>
                </tr>
              </thead>
              <tbody>
                {jobs.map((job) => (
                  <tr key={job.id}>
                    <td>{job.title}</td>
                    <td>{job.company || "—"}</td>
                    <td>{job.location || "—"}</td>
                    <td>{job.source || "—"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {jobCount === 0 && (
          <div className="card">
            <h2>No jobs yet</h2>
            <p style={{ color: "var(--text-muted)" }}>
              Upload your resume to get started. We&apos;ll find matching jobs automatically.
            </p>
            <button
              className="btn btn-primary"
              style={{ marginTop: "1rem" }}
              onClick={() => router.push("/resume")}
            >
              Upload Resume
            </button>
          </div>
        )}
      </div>
    </>
  );
}
