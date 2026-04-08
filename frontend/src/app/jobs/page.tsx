'use client';

import { useEffect, useState } from 'react';
import api from '@/lib/api';

type JobItem = { id: number; keyword_group: string; job_data: string };

export default function JobsPage() {
  const [jobs, setJobs] = useState<JobItem[]>([]);

  useEffect(() => {
    api.get('/api/jobs').then((res) => setJobs(res.data || [])).catch(() => setJobs([]));
  }, []);

  return (
    <main>
      <h1>Jobs</h1>
      <ul>
        {jobs.map((job) => (
          <li key={job.id}>{job.keyword_group}: {job.job_data}</li>
        ))}
      </ul>
    </main>
  );
}
