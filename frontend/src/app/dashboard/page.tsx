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
  total_jobs: number;
  jobs_unlocked: number;
  subscription_status: 'FREE' | 'PAID';
  plan: string;
  upgrade_required: boolean;
  upgrade_message: string;
};

export default function DashboardPage() {
  const [jobs, setJobs] = useState<JobItem[]>([]);
  const [summary, setSummary] = useState<DashboardData | null>(null);
  const [message, setMessage] = useState('Loading...');
  const [paymentMessage, setPaymentMessage] = useState('');
  const [upgrading, setUpgrading] = useState(false);

  const loadData = async () => {
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

  useEffect(() => {
    const scriptId = 'razorpay-checkout-js';
    if (!document.getElementById(scriptId)) {
      const script = document.createElement('script');
      script.id = scriptId;
      script.src = 'https://checkout.razorpay.com/v1/checkout.js';
      script.async = true;
      document.body.appendChild(script);
    }
    loadData();
  }, []);

  const upgradeToPaid = async () => {
    const email = getEmail();
    if (!email) {
      setPaymentMessage('Please login first');
      return;
    }
    setUpgrading(true);
    setPaymentMessage('');
    try {
      const orderResponse = await api.post('/api/payment/create-order', { email });
      const order = orderResponse.data;
      const razorpayCtor = (window as unknown as { Razorpay?: new (options: Record<string, unknown>) => { open: () => void } }).Razorpay;
      if (!razorpayCtor) {
        setPaymentMessage('Razorpay checkout script not available');
        return;
      }
      const instance = new razorpayCtor({
        key: order.key_id,
        amount: order.amount * 100,
        currency: order.currency,
        name: 'SAP Job SaaS',
        description: `Upgrade to ${order.plan} plan`,
        order_id: order.order_id,
        prefill: { email },
        handler: async (response: { razorpay_order_id: string; razorpay_payment_id: string; razorpay_signature: string }) => {
          try {
            await api.post('/api/payment/verify', {
              email,
              razorpay_order_id: response.razorpay_order_id,
              razorpay_payment_id: response.razorpay_payment_id,
              razorpay_signature: response.razorpay_signature,
            });
            setPaymentMessage('Payment successful. Plan upgraded.');
            await loadData();
          } catch {
            setPaymentMessage('Payment verification failed');
          }
        },
      });
      instance.open();
    } catch (error: unknown) {
      const detail =
        typeof error === 'object' &&
        error !== null &&
        'response' in error &&
        typeof (error as { response?: { data?: { detail?: string } } }).response?.data?.detail === 'string'
          ? (error as { response?: { data?: { detail?: string } } }).response?.data?.detail
          : undefined;
      setPaymentMessage(detail ?? 'Unable to start payment flow');
    } finally {
      setUpgrading(false);
    }
  };

  return (
    <main>
      <h1>Dashboard</h1>
      <p>Status: {summary?.subscription_status ?? 'N/A'} ({summary?.plan ?? 'N/A'})</p>
      <p>Jobs unlocked: {summary?.jobs_unlocked ?? jobs.length} / {summary?.total_jobs ?? jobs.length}</p>
      <p>You are eligible for {summary?.job_count ?? jobs.length} jobs</p>
      <p>Keyword Set: {summary?.keyword_set_id ?? 'N/A'}</p>
      <p>Keywords: {(summary?.keywords || []).join(', ') || 'N/A'}</p>
      {summary?.upgrade_required ? <p>{summary.upgrade_message}</p> : null}
      {summary?.subscription_status !== 'PAID' ? (
        <button type='button' onClick={upgradeToPaid} disabled={upgrading}>
          {upgrading ? 'Starting payment...' : 'Upgrade Plan'}
        </button>
      ) : null}
      <p>{paymentMessage}</p>
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
