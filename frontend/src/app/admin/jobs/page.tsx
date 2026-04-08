"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import NavBar from "@/components/NavBar";
import { getMe, getAdminJobs, isLoggedIn } from "@/lib/api";

interface Job {
  id: number;
  title: string;
  company: string | null;
  location: string | null;
  email: string | null;
  post_url: string | null;
  source: string | null;
  created_at: string;
}

export default function AdminJobsPage() {
  const router = useRouter();
  const [jobs, setJobs] = useState<Job[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);

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
        const data = await getAdminJobs();
        setTotal(data.total);
        setJobs(data.jobs);
      } catch {
        router.replace("/admin/login");
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [router]);

  if (loading) return <div className="loading">Loading jobs...</div>;

  return (
    <>
      <NavBar isAdmin />
      <div className="page-container">
        <h1>All Jobs</h1>
        <p style={{ color: "var(--text-muted)", marginBottom: "1.5rem" }}>
          {total} total job{total !== 1 ? "s" : ""} in the system
        </p>

        <div className="card" style={{ overflow: "auto" }}>
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Title</th>
                <th>Company</th>
                <th>Location</th>
                <th>Source</th>
                <th>Date</th>
              </tr>
            </thead>
            <tbody>
              {jobs.map((job) => (
                <tr key={job.id}>
                  <td>{job.id}</td>
                  <td>
                    {job.post_url ? (
                      <a href={job.post_url} target="_blank" rel="noopener noreferrer">
                        {job.title}
                      </a>
                    ) : (
                      job.title
                    )}
                  </td>
                  <td>{job.company || "—"}</td>
                  <td>{job.location || "—"}</td>
                  <td>{job.source || "—"}</td>
                  <td>{new Date(job.created_at).toLocaleDateString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </>
  );
}
