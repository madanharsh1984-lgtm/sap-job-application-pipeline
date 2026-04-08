"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import NavBar from "@/components/NavBar";
import { onboard, isLoggedIn } from "@/lib/api";

export default function ResumePage() {
  const router = useRouter();
  const [resumeText, setResumeText] = useState("");
  const [result, setResult] = useState<{
    message: string;
    keywords: string[];
    is_new_keyword_set: boolean;
  } | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!isLoggedIn()) {
      router.replace("/login");
    }
  }, [router]);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setResult(null);

    if (resumeText.trim().length < 50) {
      setError("Resume text must be at least 50 characters");
      return;
    }

    setLoading(true);
    try {
      const data = await onboard(resumeText);
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Upload failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
      <NavBar />
      <div className="page-container">
        <h1>Resume Upload</h1>
        <p style={{ color: "var(--text-muted)", marginBottom: "1.5rem" }}>
          Paste your resume text below. We&apos;ll extract keywords and find matching jobs.
        </p>

        {error && <div className="error-msg">{error}</div>}

        {result && (
          <div className="card" style={{ borderColor: "var(--success)" }}>
            <h3 style={{ color: "var(--success)" }}>✓ {result.message}</h3>
            <p style={{ marginTop: "0.5rem" }}>
              <strong>Extracted keywords:</strong>{" "}
              {result.keywords.join(", ")}
            </p>
            <button
              className="btn btn-primary"
              style={{ marginTop: "1rem" }}
              onClick={() => router.push("/dashboard")}
            >
              Go to Dashboard
            </button>
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="resume">Resume Text</label>
            <textarea
              id="resume"
              rows={12}
              value={resumeText}
              onChange={(e) => setResumeText(e.target.value)}
              placeholder="Paste your full resume text here..."
            />
          </div>
          <button type="submit" className="btn btn-primary" disabled={loading}>
            {loading ? "Processing..." : "Upload & Analyze"}
          </button>
        </form>
      </div>
    </>
  );
}
