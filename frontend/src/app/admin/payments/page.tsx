"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import NavBar from "@/components/NavBar";
import { getMe, isLoggedIn } from "@/lib/api";

export default function AdminPaymentsPage() {
  const router = useRouter();

  useEffect(() => {
    if (!isLoggedIn()) {
      router.replace("/admin/login");
      return;
    }

    async function checkAdmin() {
      try {
        const me = await getMe();
        if (me.role !== "admin") {
          router.replace("/dashboard");
        }
      } catch {
        router.replace("/admin/login");
      }
    }
    checkAdmin();
  }, [router]);

  return (
    <>
      <NavBar isAdmin />
      <div className="page-container">
        <h1>Payments</h1>
        <p style={{ color: "var(--text-muted)", marginBottom: "1.5rem" }}>
          Payment tracking and subscription management.
        </p>

        <div className="card">
          <h3>Coming Soon</h3>
          <p style={{ color: "var(--text-muted)" }}>
            Payment integration is being developed. You&apos;ll be able to view
            subscription status, payment history, and manage billing here.
          </p>
        </div>
      </div>
    </>
  );
}
