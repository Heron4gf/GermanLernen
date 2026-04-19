import { ref } from 'vue'
import { api } from '../api.js'

const cards   = ref([])
const loading = ref(false)
const error   = ref(null)

async function load() {
  if (cards.value.length > 0) return   // already fetched
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

export function useCards() {
  return { cards, loading, error, load }
}