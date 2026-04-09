'use client';

import { useState } from 'react';
import api from '@/lib/api';
import { getEmail, setKeywordSetId } from '@/lib/auth';

export default function ResumePage() {
  const [content, setContent] = useState('');
  const [file, setFile] = useState<File | null>(null);
  const [message, setMessage] = useState('');

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    const email = getEmail();
    if (!email) {
      setMessage('Please login first');
      return;
    }
    try {
      const formData = new FormData();
      formData.append('email', email);
      if (content) formData.append('content', content);
      if (file) formData.append('file', file);

      const response = await api.post('/api/user/onboard', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      if (response.data.keyword_set_id) {
        setKeywordSetId(String(response.data.keyword_set_id));
      }
      setMessage(
        `Resume uploaded. Keywords: ${(response.data.keywords || []).join(', ')} ${
          response.data.upgrade_message ? `| ${response.data.upgrade_message}` : ''
        }`
      );
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
