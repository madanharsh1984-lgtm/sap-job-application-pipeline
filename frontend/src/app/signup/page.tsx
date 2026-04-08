'use client';

import { useState } from 'react';
import api from '@/lib/api';
import { setEmail as setSessionEmail, setKeywordSetId } from '@/lib/auth';

export default function SignupPage() {
  const [email, setEmailInput] = useState('');
  const [resumeContent, setResumeContent] = useState('');
  const [resumeFile, setResumeFile] = useState<File | null>(null);
  const [message, setMessage] = useState('');

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const formData = new FormData();
      formData.append('email', email);
      if (resumeContent.trim()) {
        formData.append('content', resumeContent);
      }
      if (resumeFile) {
        formData.append('file', resumeFile);
      }

      const onboardResponse = await api.post('/api/user/onboard', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      if (onboardResponse.data?.keyword_set_id) {
        setKeywordSetId(String(onboardResponse.data.keyword_set_id));
      }
      setSessionEmail(email);
      setMessage('Signup and onboarding successful. Redirecting to dashboard...');
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
        <input aria-label='Email' value={email} onChange={(e) => setEmailInput(e.target.value)} placeholder='Email' required />
        <br />
        <textarea
          aria-label='Resume content'
          value={resumeContent}
          onChange={(e) => setResumeContent(e.target.value)}
          placeholder='Paste resume text'
          rows={6}
        />
        <br />
        <input aria-label='Resume file' type='file' accept='.txt,.pdf,.doc,.docx' onChange={(e) => setResumeFile(e.target.files?.[0] ?? null)} />
        <br />
        <button type='submit'>Create account</button>
      </form>
      <p>{message}</p>
    </main>
  );
}
