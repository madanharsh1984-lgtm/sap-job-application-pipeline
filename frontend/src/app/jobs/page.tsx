"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import NavBar from "@/components/NavBar";
import { getJobs, isLoggedIn } from "@/lib/api";

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

export default function JobsPage() {
  const router = useRouter();
  const [jobs, setJobs] = useState<Job[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!isLoggedIn()) {
      router.replace("/login");
      return;
    }

    async function load() {
      try {
        const data = await getJobs();
        setTotal(data.total);
        setJobs(data.jobs);
      } catch {
        router.replace("/login");
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [router]);

  if (loading) return <div className="loading">Loading jobs...</div>;

  return (
    <>
      <NavBar />
      <div className="page-container">
        <h1>Qualified Jobs</h1>
        <p style={{ color: "var(--text-muted)", marginBottom: "1.5rem" }}>
          {total} job{total !== 1 ? "s" : ""} matched to your resume keywords
        </p>

        {jobs.length === 0 ? (
          <div className="card">
            <p>No qualified jobs found. Upload or update your resume to find matches.</p>
            <button
              className="btn btn-primary"
              style={{ marginTop: "1rem" }}
              onClick={() => router.push("/resume")}
            >
              Update Resume
            </button>
          </div>
        ) : (
          <div className="card" style={{ overflow: "auto" }}>
            <table>
              <thead>
                <tr>
                  <th>Title</th>
                  <th>Company</th>
                  <th>Location</th>
                  <th>Contact</th>
                  <th>Source</th>
                  <th>Date</th>
                </tr>
              </thead>
              <tbody>
                {jobs.map((job) => (
                  <tr key={job.id}>
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
                    <td>{job.email || "—"}</td>
                    <td>{job.source || "—"}</td>
                    <td>{new Date(job.created_at).toLocaleDateString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </>
  );
}
