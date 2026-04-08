'use client';

import { clearToken, getToken } from '@/lib/auth';

export default function AccountPage() {
  const token = getToken();

  return (
    <main>
      <h1>Account</h1>
      <p>JWT token is {token ? 'present' : 'not set'}.</p>
      <button
        onClick={() => {
          clearToken();
          window.location.href = '/login';
        }}
      >
        Logout
      </button>
    </main>
  );
}
