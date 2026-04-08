'use client';

import { useState } from 'react';
import api from '@/lib/api';

export default function ResumePage() {
  const [content, setContent] = useState('');
  const [file, setFile] = useState<File | null>(null);
  const [message, setMessage] = useState('');

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const formData = new FormData();
      if (content) formData.append('content', content);
      if (file) formData.append('file', file);

      const response = await api.post('/api/user/onboard', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setMessage(`Resume uploaded. Keywords: ${(response.data.keywords || []).join(', ')}`);
    } catch {
      setMessage('Resume upload failed');
    }
  };

  return (
    <main>
      <h1>Resume Onboarding</h1>
      <form onSubmit={submit}>
        <input type='file' accept='.txt,.md,.doc,.docx,.pdf' onChange={(e) => setFile(e.target.files?.[0] || null)} />
        <br />
        <p>Or paste resume content:</p>
        <textarea value={content} onChange={(e) => setContent(e.target.value)} rows={10} cols={80} />
        <br />
        <button type='submit'>Upload resume</button>
      </form>
      <p>{message}</p>
    </main>
  );
}
