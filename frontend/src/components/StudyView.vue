<template>
  <div>
    <div v-if="loading" class="page-header">
      <div class="skeleton skeleton-line w-40 skeleton-title"></div>
      <div class="skeleton skeleton-line w-60 skeleton-subtitle"></div>
    </div>

    <div v-else-if="error" class="empty-state">
      <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true">
        <circle cx="12" cy="12" r="10"/>
        <line x1="12" y1="8" x2="12" y2="12"/>
        <line x1="12" y1="16" x2="12.01" y2="16"/>
      </svg>
      <h3>Could not load card</h3>
      <p>{{ error }}</p>
    </div>

    <template v-else-if="card">
      <div class="page-header">
        <div class="header-title-group">
          <h1 class="page-title">{{ card.title }}</h1>
          <span class="badge badge-teal">{{ card.words.length }} words</span>
        </div>
        <div class="mode-toggle" role="group" aria-label="Study mode">
          <button
            class="mode-btn"
            :class="{ active: mode === 'learn' }"
            @click="mode = 'learn'"
          >Learn</button>
          <button
            class="mode-btn"
            :class="{ active: mode === 'exercise' }"
            @click="mode = 'exercise'"
          >Exercise</button>
        </div>
      </div>

      <transition name="slide" mode="out-in">
        <div v-if="mode === 'learn'" key="learn" class="card">
          <div class="card-body card-body-no-padding">
            <WordTable :words="card.words" />
          </div>
        </div>
        <div v-else key="exercise">
          <ExerciseMode :words="card.words" />
        </div>
      </transition>
    </template>

    <div v-else class="empty-state">
      <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true">
        <path d="M9 11l3 3L22 4"/>
        <path d="M21 12v7a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2h11"/>
      </svg>
      <h3>No card yet</h3>
      <p>The daemon will generate the first card within 24 hours.</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import WordTable from './WordTable.vue'
import ExerciseMode from './ExerciseMode.vue'

defineProps({
  card:    { type: Object, default: null },
  loading: { type: Boolean, default: false },
  error:   { type: String,  default: null },
})

const mode = ref('learn')
</script>

<style scoped>
.skeleton-title {
  height: 2rem;
  margin-bottom: var(--space-2);
}

.skeleton-subtitle {
  height: 1rem;
}

.header-title-group {
  display: flex;
  align-items: baseline;
  gap: var(--space-3);
  flex-wrap: wrap;
  margin-bottom: var(--space-5);
}

.card-body-no-padding {
  padding: 0;
}
</style>