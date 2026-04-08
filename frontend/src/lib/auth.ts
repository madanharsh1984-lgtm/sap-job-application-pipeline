const TOKEN_KEY = 'sap_mvp_token';
const EMAIL_KEY = 'sap_mvp_email';
const KEYWORD_SET_KEY = 'sap_mvp_keyword_set_id';

export function getToken(): string | null {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem(TOKEN_KEY);
}

export function setToken(token: string): void {
  if (typeof window === 'undefined') return;
  localStorage.setItem(TOKEN_KEY, token);
}

export function clearToken(): void {
  if (typeof window === 'undefined') return;
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(EMAIL_KEY);
  localStorage.removeItem(KEYWORD_SET_KEY);
}

export function getEmail(): string | null {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem(EMAIL_KEY);
}

export function setEmail(email: string): void {
  if (typeof window === 'undefined') return;
  localStorage.setItem(EMAIL_KEY, email);
}

export function getKeywordSetId(): string | null {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem(KEYWORD_SET_KEY);
}

export function setKeywordSetId(keywordSetId: string): void {
  if (typeof window === 'undefined') return;
  localStorage.setItem(KEYWORD_SET_KEY, keywordSetId);
}
