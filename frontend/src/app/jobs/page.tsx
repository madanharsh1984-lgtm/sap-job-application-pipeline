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

export default function JobsPage() {
  const [jobs, setJobs] = useState<JobItem[]>([]);
  const [message, setMessage] = useState('Loading...');

  useEffect(() => {
    const email = getEmail();
    if (!email) {
      setJobs([]);
      setMessage('Please login first');
      return;
    }
    api
      .get('/api/jobs', { params: { email } })
      .then((res) => {
        setJobs(Array.isArray(res.data) ? res.data : []);
        setMessage('Loaded');
      })
      .catch(() => {
        setJobs([]);
        setMessage('Unable to fetch jobs');
      });
  }, []);

  return (
    <main>
      <h1>Jobs</h1>
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
