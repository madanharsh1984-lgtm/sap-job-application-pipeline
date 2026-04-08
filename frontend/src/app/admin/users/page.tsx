"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import NavBar from "@/components/NavBar";
import { getMe, getAdminUsers, isLoggedIn } from "@/lib/api";

interface AdminUser {
  id: number;
  email: string;
  role: string;
  created_at: string;
  resume_count: number;
  keyword_set_count: number;
}

export default function AdminUsersPage() {
  const router = useRouter();
  const [users, setUsers] = useState<AdminUser[]>([]);
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
        const data = await getAdminUsers();
        setTotal(data.total);
        setUsers(data.users);
      } catch {
        router.replace("/admin/login");
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [router]);

  if (loading) return <div className="loading">Loading users...</div>;

  return (
    <>
      <NavBar isAdmin />
      <div className="page-container">
        <h1>User Management</h1>
        <p style={{ color: "var(--text-muted)", marginBottom: "1.5rem" }}>
          {total} registered user{total !== 1 ? "s" : ""}
        </p>

        <div className="card" style={{ overflow: "auto" }}>
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Email</th>
                <th>Role</th>
                <th>Resumes</th>
                <th>Keyword Sets</th>
                <th>Joined</th>
              </tr>
            </thead>
            <tbody>
              {users.map((u) => (
                <tr key={u.id}>
                  <td>{u.id}</td>
                  <td>{u.email}</td>
                  <td>
                    <span className={`badge ${u.role === "admin" ? "badge-admin" : "badge-user"}`}>
                      {u.role}
                    </span>
                  </td>
                  <td>{u.resume_count}</td>
                  <td>{u.keyword_set_count}</td>
                  <td>{new Date(u.created_at).toLocaleDateString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </>
  );
}
