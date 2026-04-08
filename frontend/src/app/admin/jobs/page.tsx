'use client';

import { useEffect, useState } from 'react';
import api from '@/lib/api';

export default function AdminJobsPage() {
  const [jobsCount, setJobsCount] = useState<number>(0);

  useEffect(() => {
    api.get('/admin/metrics').then((res) => setJobsCount(res.data?.jobs_count || 0)).catch(() => setJobsCount(0));
  }, []);

  return (
    <main>
      <h1>Admin Jobs</h1>
      <p>Total jobs in system: {jobsCount}</p>
    </main>
  );
}
