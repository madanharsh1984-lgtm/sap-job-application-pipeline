'use client';

import { useEffect, useState } from 'react';
import api from '@/lib/api';
import { getEmail, setKeywordSetId } from '@/lib/auth';

type JobItem = {
  id?: string;
  title?: string;
  company?: string;
  location?: string;
  url?: string;
  source?: string;
};

type DashboardData = {
  email: string;
  keyword_set_id: string;
  keywords: string[];
  job_count: number;
};

export default function DashboardPage() {
  const [jobs, setJobs] = useState<JobItem[]>([]);
  const [summary, setSummary] = useState<DashboardData | null>(null);
  const [message, setMessage] = useState('Loading...');

  useEffect(() => {
    const load = async () => {
      const email = getEmail();
      if (!email) {
        setMessage('Please login first');
        setJobs([]);
        setSummary(null);
        return;
      }
      try {
        const [dashboardResponse, jobsResponse] = await Promise.all([
          api.get('/api/dashboard', { params: { email } }),
          api.get('/api/jobs', { params: { email } }),
        ]);
        setSummary(dashboardResponse.data);
        if (dashboardResponse.data?.keyword_set_id) {
          setKeywordSetId(String(dashboardResponse.data.keyword_set_id));
        }
        setJobs(Array.isArray(jobsResponse.data) ? jobsResponse.data : []);
        setMessage('Loaded');
      } catch (error: unknown) {
        const detail =
          typeof error === 'object' &&
          error !== null &&
          'response' in error &&
          typeof (error as { response?: { data?: { detail?: string } } }).response?.data?.detail === 'string'
            ? (error as { response?: { data?: { detail?: string } } }).response?.data?.detail
            : undefined;
        setMessage(detail ?? 'Unable to fetch jobs');
        setJobs([]);
        setSummary(null);
      }
    };
    load();
  }, []);

  return (
    <main>
      <h1>Dashboard</h1>
      <p>You are eligible for {summary?.job_count ?? jobs.length} jobs</p>
      <p>Keyword Set: {summary?.keyword_set_id ?? 'N/A'}</p>
      <p>Keywords: {(summary?.keywords || []).join(', ') || 'N/A'}</p>
      <p>{message}</p>
      <table border={1} cellPadding={8}>
        <thead>
          <tr>
            <th>Title</th>
            <th>Company</th>
            <th>Location</th>
            <th>Source</th>
            <th>URL</th>
          </tr>
        </thead>
        <tbody>
          {jobs.map((job) => (
            <tr key={job.id || job.url || `${job.title}-${job.company}`}>
              <td>{job.title || 'N/A'}</td>
              <td>{job.company || 'N/A'}</td>
              <td>{job.location || 'N/A'}</td>
              <td>{job.source || 'N/A'}</td>
              <td>{job.url ? <a href={job.url} target='_blank' rel='noreferrer'>Open</a> : 'N/A'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </main>
  );
}
