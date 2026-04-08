'use client';

import { useEffect, useState } from 'react';
import api from '@/lib/api';

type JobItem = { id: number; keyword_set_id: number; job_data: string };

export default function DashboardPage() {
  const [jobs, setJobs] = useState<JobItem[]>([]);
  const [message, setMessage] = useState('Loading...');

  useEffect(() => {
    const load = async () => {
      try {
        const response = await api.get('/api/jobs');
        setJobs(response.data || []);
        setMessage('Loaded');
      } catch {
        setMessage('Unable to fetch jobs');
      }
    };
    load();
  }, []);

  return (
    <main>
      <h1>Dashboard</h1>
      <p>You are eligible for {jobs.length} jobs</p>
      <p>{message}</p>
      <table border={1} cellPadding={8}>
        <thead>
          <tr>
            <th>ID</th>
            <th>Keyword Group</th>
            <th>Job Data</th>
          </tr>
        </thead>
        <tbody>
          {jobs.map((job) => (
            <tr key={job.id}>
              <td>{job.id}</td>
              <td>{job.keyword_set_id}</td>
              <td>{job.job_data}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </main>
  );
}
