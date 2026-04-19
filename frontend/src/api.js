async function request(path) {
  const res = await fetch(path)
  if (!res.ok) throw new Error(`HTTP ${res.status}`)
  return res.json()
}

export const api = {
  getLatestCard: () => request('/cards/latest'),
  getCards:      () => request('/cards'),
}