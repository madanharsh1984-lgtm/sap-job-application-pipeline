'use client';

import { useEffect, useState } from 'react';
import api from '@/lib/api';
import { getEmail } from '@/lib/auth';

type JobItem = {
  id?: string;
  title?: string;
  company?: string;
  location?: string;
  url?: string;
  source?: string;
};

type DashboardData = {
  subscription_status: 'FREE' | 'PAID';
  jobs_unlocked: number;
  total_jobs: number;
  upgrade_required: boolean;
  upgrade_message: string;
};

export default function JobsPage() {
  const [jobs, setJobs] = useState<JobItem[]>([]);
  const [summary, setSummary] = useState<DashboardData | null>(null);
  const [message, setMessage] = useState('Loading...');

  useEffect(() => {
    const email = getEmail();
    if (!email) {
      setJobs([]);
      setMessage('Please login first');
      return;
    }
    Promise.all([
      api.get('/api/jobs', { params: { email } }),
      api.get('/api/dashboard', { params: { email } }),
    ])
      .then(([jobsResponse, dashboardResponse]) => {
        setJobs(Array.isArray(jobsResponse.data) ? jobsResponse.data : []);
        setSummary(dashboardResponse.data);
        setMessage('Loaded');
      })
      .catch(() => {
        setJobs([]);
        setSummary(null);
        setMessage('Unable to fetch jobs');
      });
  }, []);

  return (
    <main>
      <h1>Jobs</h1>
      <p>Status: {summary?.subscription_status ?? 'N/A'}</p>
      <p>Visible jobs: {summary?.jobs_unlocked ?? jobs.length} / {summary?.total_jobs ?? jobs.length}</p>
      {summary?.upgrade_required ? <p>{summary.upgrade_message}</p> : null}
      <p>{message}</p>
      <ul>
        {jobs.map((job) => (
          <li key={job.id || job.url || `${job.title}-${job.company}`}>
            {job.title || 'N/A'} | {job.company || 'N/A'} | {job.location || 'N/A'} | {job.url ? <a href={job.url} target='_blank' rel='noreferrer'>Open</a> : 'N/A'}
          </li>
        ))}
      </ul>
    </main>
  );
}
