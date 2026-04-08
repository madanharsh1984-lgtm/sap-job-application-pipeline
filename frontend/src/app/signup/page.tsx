'use client';

import { useState } from 'react';
import api from '@/lib/api';
import { setToken } from '@/lib/auth';

export default function SignupPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await api.post('/api/auth/register', { email, password });
      setToken(response.data.access_token);
      setMessage('Signup successful. Redirecting to dashboard...');
      window.location.href = '/dashboard';
    } catch (error: unknown) {
      const detail =
        typeof error === 'object' &&
        error !== null &&
        'response' in error &&
        typeof (error as { response?: { data?: { detail?: string } } }).response?.data?.detail === 'string'
          ? (error as { response?: { data?: { detail?: string } } }).response?.data?.detail
          : undefined;
      setMessage(detail ?? 'Signup failed');
    }
  };

  return (
    <main>
      <h1>Signup</h1>
      <form onSubmit={submit}>
        <input value={email} onChange={(e) => setEmail(e.target.value)} placeholder='Email' required />
        <br />
        <input value={password} onChange={(e) => setPassword(e.target.value)} type='password' placeholder='Password' required />
        <br />
        <button type='submit'>Create account</button>
      </form>
      <p>{message}</p>
    </main>
  );
}
