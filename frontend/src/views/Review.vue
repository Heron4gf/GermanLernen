<template>
  <main class="page">
    <div class="container container--narrow">
      <router-link to="/history" class="back-link">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M15 18l-6-6 6-6"/></svg>
        Back to History
      </router-link>
      <StudyView :card="card" :loading="loading" :error="error" />
    </div>
  </main>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useCard } from '../composables/useCard.js'
import { api } from '../api.js'
import StudyView from '../components/StudyView.vue'

const route = useRoute()

// The /cards endpoint already fetches everything client-side.
// We find the card from the full list by id — no extra endpoint needed.
const { card, loading, error, load } = useCard(async () => {
  const all = await api.getCards()
  const found = all.find(c => c.id === route.params.id)
  if (!found) throw new Error('Card not found')
  return found
})

onMounted(load)
</script>
