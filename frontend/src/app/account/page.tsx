"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import NavBar from "@/components/NavBar";
import { getMe, isLoggedIn } from "@/lib/api";

interface User {
  id: number;
  email: string;
  role: string;
  created_at: string;
}

export default function AccountPage() {
  const router = useRouter();
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!isLoggedIn()) {
      router.replace("/login");
      return;
    }

    async function load() {
      try {
        const me = await getMe();
        setUser(me);
      } catch {
        router.replace("/login");
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [router]);

  if (loading) return <div className="loading">Loading...</div>;

  return (
    <>
      <NavBar />
      <div className="page-container">
        <h1>Account Details</h1>

        <div className="card">
          <div className="form-group">
            <label>Email</label>
            <input type="text" value={user?.email || ""} disabled />
          </div>
          <div className="form-group">
            <label>Role</label>
            <input type="text" value={user?.role || ""} disabled />
          </div>
          <div className="form-group">
            <label>Member Since</label>
            <input
              type="text"
              value={user?.created_at ? new Date(user.created_at).toLocaleDateString() : ""}
              disabled
            />
          </div>
        </div>
      </div>
    </>
  );
}
