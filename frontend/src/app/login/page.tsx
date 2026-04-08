'use client';

import { useState } from 'react';
import api from '@/lib/api';
import { setEmail as setSessionEmail, setKeywordSetId } from '@/lib/auth';

export default function LoginPage() {
  const [email, setEmailInput] = useState('');
  const [message, setMessage] = useState('');

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await api.get('/api/dashboard', { params: { email } });
      setSessionEmail(email);
      if (response.data?.keyword_set_id) {
        setKeywordSetId(String(response.data.keyword_set_id));
      }
      setMessage('Login successful. Redirecting to dashboard...');
      window.location.href = '/dashboard';
    } catch (error: unknown) {
      const detail =
        typeof error === 'object' &&
        error !== null &&
        'response' in error &&
        typeof (error as { response?: { data?: { detail?: string } } }).response?.data?.detail === 'string'
          ? (error as { response?: { data?: { detail?: string } } }).response?.data?.detail
          : undefined;
      setMessage(detail ?? 'Login failed');
    }
  };

  return (
    <main>
      <h1>Login</h1>
      <form onSubmit={submit}>
        <input aria-label='Email' value={email} onChange={(e) => setEmailInput(e.target.value)} placeholder='Email' required />
        <br />
        <button type='submit'>Login</button>
      </form>
      <p>{message}</p>
    </main>
  );
}
