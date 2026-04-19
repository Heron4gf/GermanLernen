const BASE = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

async function request(path) {
  const res = await fetch(`${BASE}${path}`)
  if (!res.ok) throw new Error(`HTTP ${res.status}`)
  return res.json()
}

export const api = {
  getLatestCard: () => request('/cards/latest'),
  getCards:      () => request('/cards'),
}
