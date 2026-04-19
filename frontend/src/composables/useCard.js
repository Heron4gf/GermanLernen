import { ref } from 'vue'
import { api } from '../api.js'

// Singleton state — created once at module level
const card    = ref(null)
const loading = ref(false)
const error   = ref(null)

async function load() {
  if (card.value !== null) return   // already fetched, skip
  loading.value = true
  error.value   = null
  try {
    card.value = await api.getLatestCard()
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

export function useCard() {
  return { card, loading, error, load }
}