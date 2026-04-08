'use client';

import { useState } from 'react';
import api from '@/lib/api';
import { setToken } from '@/lib/auth';

export default function AdminLoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await api.post('/api/auth/login', { email, password });
      setToken(response.data.access_token);
      setMessage('Login successful. Redirecting to admin dashboard...');
      window.location.href = '/admin/dashboard';
    } catch (error: any) {
      setMessage(error?.response?.data?.detail || 'Admin login failed');
    }
  };

  return (
    <main>
      <h1>Admin Login</h1>
      <form onSubmit={submit}>
        <input value={email} onChange={(e) => setEmail(e.target.value)} placeholder='Admin Email' required />
        <br />
        <input value={password} onChange={(e) => setPassword(e.target.value)} type='password' placeholder='Password' required />
        <br />
        <button type='submit'>Login</button>
      </form>
      <p>{message}</p>
    </main>
  );
}
