"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import NavBar from "@/components/NavBar";
import { isLoggedIn } from "@/lib/api";

export default function ConnectionsPage() {
  const router = useRouter();

  useEffect(() => {
    if (!isLoggedIn()) {
      router.replace("/login");
    }
  }, [router]);

  return (
    <>
      <NavBar />
      <div className="page-container">
        <h1>Connections</h1>
        <p style={{ color: "var(--text-muted)", marginBottom: "1.5rem" }}>
          Manage your professional connections and outreach.
        </p>

        <div className="card">
          <h3>Coming Soon</h3>
          <p style={{ color: "var(--text-muted)" }}>
            Connection management is being developed. You&apos;ll be able to track
            recruiter connections and outreach history here.
          </p>
        </div>
      </div>
    </>
  );
}
