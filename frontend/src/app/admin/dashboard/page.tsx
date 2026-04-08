'use client';

import { useEffect, useState } from 'react';
import api from '@/lib/api';

export default function AdminDashboardPage() {
  const [metrics, setMetrics] = useState<{ users_count: number; jobs_count: number; resumes_count: number } | null>(null);

  useEffect(() => {
    api.get('/admin/metrics').then((res) => setMetrics(res.data)).catch(() => setMetrics(null));
  }, []);

  return (
    <main>
      <h1>Admin Dashboard</h1>
      {metrics ? (
        <ul>
          <li>Total users: {metrics.users_count}</li>
          <li>Total jobs: {metrics.jobs_count}</li>
          <li>Total resumes: {metrics.resumes_count}</li>
        </ul>
      ) : (
        <p>Unable to load metrics (admin role required).</p>
      )}
    </main>
  );
}
