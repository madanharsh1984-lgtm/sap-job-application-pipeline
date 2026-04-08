'use client';

import { useState } from 'react';
import api from '@/lib/api';

export default function ResumePage() {
  const [content, setContent] = useState('');
  const [message, setMessage] = useState('');

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await api.post('/api/user/onboard', { content });
      setMessage(`Resume uploaded. Keywords: ${(response.data.keywords || []).join(', ')}`);
    } catch {
      setMessage('Resume upload failed');
    }
  };

  return (
    <main>
      <h1>Resume Onboarding</h1>
      <form onSubmit={submit}>
        <textarea value={content} onChange={(e) => setContent(e.target.value)} rows={10} cols={80} required />
        <br />
        <button type='submit'>Upload resume</button>
      </form>
      <p>{message}</p>
    </main>
  );
}
