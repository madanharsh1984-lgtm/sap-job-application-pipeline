const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export function getToken(): string | null {
  if (typeof window === 'undefined') return null
  return localStorage.getItem('token')
}

export function setToken(token: string): void {
  localStorage.setItem('token', token)
}

export function removeToken(): void {
  localStorage.removeItem('token')
}

export async function apiRequest(
  endpoint: string,
  options: RequestInit = {}
): Promise<Response> {
  const token = getToken()
  const headers: HeadersInit = {
    ...options.headers,
  }

  if (token) {
    ;(headers as Record<string, string>)['Authorization'] = `Bearer ${token}`
  }

  if (
    options.body &&
    typeof options.body === 'string' &&
    !(headers as Record<string, string>)['Content-Type']
  ) {
    ;(headers as Record<string, string>)['Content-Type'] = 'application/json'
  }

  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers,
  })

  if (response.status === 401) {
    removeToken()
    if (typeof window !== 'undefined') {
      window.location.href = '/login'
    }
  }

  return response
}

export async function apiGet(endpoint: string): Promise<Response> {
  return apiRequest(endpoint, { method: 'GET' })
}

export async function apiPost(
  endpoint: string,
  data: unknown
): Promise<Response> {
  return apiRequest(endpoint, {
    method: 'POST',
    body: JSON.stringify(data),
    headers: { 'Content-Type': 'application/json' },
  })
}

export async function apiPut(
  endpoint: string,
  data: unknown
): Promise<Response> {
  return apiRequest(endpoint, {
    method: 'PUT',
    body: JSON.stringify(data),
    headers: { 'Content-Type': 'application/json' },
  })
}

export async function apiDelete(endpoint: string): Promise<Response> {
  return apiRequest(endpoint, { method: 'DELETE' })
}
