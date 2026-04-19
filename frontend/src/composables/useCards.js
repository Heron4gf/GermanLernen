import { ref } from 'vue'
import { api } from '../api.js'

export function useCards() {
  const cards   = ref([])
  const loading = ref(false)
  const error   = ref(null)

  async function load() {
    loading.value = true
    error.value   = null
    try {
      cards.value = await api.getCards()
    } catch (e) {
      error.value = e.message
    } finally {
      loading.value = false
    }
  }

  return { cards, loading, error, load }
}
