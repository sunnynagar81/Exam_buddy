export const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
const TOKEN_KEY = 'exam_buddy_token'

export function saveToken(token) {
  localStorage.setItem(TOKEN_KEY, token)
}

export function getToken() {
  return localStorage.getItem(TOKEN_KEY)
}

export function logout() {
  localStorage.removeItem(TOKEN_KEY)
}

function authHeaders(extra = {}) {
  const token = getToken()
  return token ? { ...extra, Authorization: `Bearer ${token}` } : extra
}

async function request(path, options = {}) {
  const res = await fetch(`${API_URL}${path}`, options)
  const data = await res.json().catch(() => ({}))
  if (!res.ok) {
    throw new Error(typeof data.detail === 'string' ? data.detail : 'Something went wrong. Please try again.')
  }
  return data
}

export function post(path, body) {
  return request(path, {
    method: 'POST',
    headers: authHeaders({ 'Content-Type': 'application/json' }),
    body: JSON.stringify(body),
  })
}

export function get(path) {
  return request(path, { headers: authHeaders() })
}

export function uploadFile(file) {
  const form = new FormData()
  form.append('file', file)
  return request('/api/upload', { method: 'POST', headers: authHeaders(), body: form })
}