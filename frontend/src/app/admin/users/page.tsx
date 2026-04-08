'use client';

import { useEffect, useState } from 'react';
import api from '@/lib/api';

type AdminUser = { id: number; email: string; role: string; created_at: string };

export default function AdminUsersPage() {
  const [users, setUsers] = useState<AdminUser[]>([]);

  useEffect(() => {
    api.get('/admin/users').then((res) => setUsers(res.data || [])).catch(() => setUsers([]));
  }, []);

  return (
    <main>
      <h1>Admin Users</h1>
      <ul>
        {users.map((user) => (
          <li key={user.id}>{user.email} ({user.role})</li>
        ))}
      </ul>
    </main>
  );
}
