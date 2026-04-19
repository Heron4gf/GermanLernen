<template>
  <main class="page">
    <div class="container container--narrow">
      <div class="page-header">
        <h1 class="page-title">History</h1>
        <p class="page-subtitle">All generated cards — click one to review it.</p>
      </div>

      <!-- Skeleton -->
      <div v-if="loading" class="history-list">
        <div v-for="i in 6" :key="i" class="card card-body">
          <div class="skeleton skeleton-line w-60" style="height:1.1rem;margin-bottom:var(--space-1)"></div>
          <div class="skeleton skeleton-line w-40" style="height:0.8rem"></div>
        </div>
      </div>

      <!-- Error -->
      <div v-else-if="error" class="empty-state">
        <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
        <h3>Failed to load history</h3>
        <p>{{ error }}</p>
      </div>

      <!-- Empty -->
      <div v-else-if="!cards.length" class="empty-state">
        <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M9 9h6M9 13h4"/></svg>
        <h3>No cards yet</h3>
        <p>Cards will appear here as the daemon generates them daily.</p>
      </div>

      <!-- List -->
      <template v-else>
        <ul role="list" class="history-list">
          <li v-for="card in paginated" :key="card.id">
            <router-link :to="`/review/${card.id}`" class="history-item">
              <div>
                <p class="history-item-title">{{ card.title }}</p>
                <p class="history-item-meta">{{ formatDate(card.createdAt) }} · {{ card.words?.length ?? '?' }} words</p>
              </div>
              <svg class="history-item-arrow" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M9 18l6-6-6-6"/></svg>
            </router-link>
          </li>
        </ul>

        <nav class="pagination" aria-label="Page navigation" v-if="totalPages > 1">
          <button class="pagination-btn" :disabled="page === 1" @click="page--" aria-label="Previous page">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M15 18l-6-6 6-6"/></svg>
          </button>
          <button
            v-for="p in totalPages" :key="p"
            class="pagination-btn"
            :class="{ active: p === page }"
            @click="page = p"
            :aria-current="p === page ? 'page' : undefined"
          >{{ p }}</button>
          <button class="pagination-btn" :disabled="page === totalPages" @click="page++" aria-label="Next page">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M9 18l6-6-6-6"/></svg>
          </button>
        </nav>
      </template>
    </div>
  </main>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useCards } from '../composables/useCards.js'

const { cards, loading, error, load } = useCards()
onMounted(load)

const PAGE_SIZE = 10
const page = ref(1)

const totalPages = computed(() => Math.ceil(cards.value.length / PAGE_SIZE))
const paginated  = computed(() => {
  const start = (page.value - 1) * PAGE_SIZE
  return cards.value.slice(start, start + PAGE_SIZE)
})

function formatDate(iso) {
  if (!iso) return ''
  return new Date(iso).toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' })
}
</script>
