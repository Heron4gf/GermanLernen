import { ref } from 'vue'
import { api } from '../api.js'

export function useCard(fetcher) {
  const card    = ref(null)
  const loading = ref(false)
  const error   = ref(null)
  const fn      = fetcher ?? api.getLatestCard

  async function load() {
    loading.value = true
    error.value   = null
    try {
      card.value = await fn()
    } catch (e) {
      error.value = e.message
    } finally {
      loading.value = false
    }
  }

  return { card, loading, error, load }
}