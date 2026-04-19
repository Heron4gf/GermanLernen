<template>
  <main class="page">
    <div class="container container--narrow">
      <StudyView :card="card" :loading="loading" :error="error" />
    </div>
  </main>
</template>

<script setup>
import { onMounted } from 'vue'
import { useCard } from '../composables/useCard.js'
import StudyView from '../components/StudyView.vue'

const { card, loading, error, load } = useCard()
onMounted(load)
</script>