<template>
  <div>
    <div class="exercise-progress">
      <div class="progress-bar" role="progressbar" :aria-valuenow="current + 1" :aria-valuemax="words.length">
        <div class="progress-fill" :style="{ width: progressPct + '%' }"></div>
      </div>
      <span class="progress-label">{{ current + 1 }}/{{ words.length }}</span>
    </div>

    <transition name="fade">
      <div v-if="done" class="card result-card">
        <p class="result-score">{{ score }}/{{ words.length }}</p>
        <p class="result-label">correct answers</p>
        <button class="btn btn-primary btn-lg" @click="restart">Try again</button>
      </div>
    </transition>

    <transition name="slide" mode="out-in">
      <div v-if="!done" :key="current" class="exercise-card">
        <p class="exercise-prompt-label">Translate to German</p>
        <p class="exercise-prompt">{{ currentWord.translation }}</p>

        <div class="exercise-input-row">
          <input
            ref="inputEl"
            v-model="answer"
            :class="['exercise-input', inputState]"
            type="text"
            placeholder="Type the German word…"
            :disabled="revealed"
            @keyup.enter="revealed ? next() : check()"
            aria-label="Your answer"
          />
          <button
            v-if="!revealed"
            class="btn btn-primary"
            @click="check"
            :disabled="!answer.trim()"
          >
            Check
          </button>
          <button v-else class="btn btn-outline" @click="next">
            {{ isLast ? 'Finish' : 'Next' }}
          </button>
        </div>

        <transition name="fade">
          <p v-if="revealed" :class="['feedback', inputState]">
            <template v-if="inputState === 'correct'">Correct!</template>
            <template v-else>Correct answer: <strong>{{ currentWord.word }}</strong></template>
          </p>
        </transition>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, nextTick } from 'vue'

const props = defineProps({ words: { type: Array, required: true } })

const current   = ref(0)
const answer    = ref('')
const revealed  = ref(false)
const inputState = ref('')
const score     = ref(0)
const done      = ref(false)
const inputEl   = ref(null)

const currentWord = computed(() => props.words[current.value])
const progressPct = computed(() => ((current.value) / props.words.length) * 100)
const isLast      = computed(() => current.value === props.words.length - 1)

function check() {
  if (!answer.value.trim()) return
  const correct = answer.value.trim().toLowerCase() === currentWord.value.word.toLowerCase()
  inputState.value = correct ? 'correct' : 'wrong'
  if (correct) score.value++
  revealed.value = true
}

function next() {
  if (isLast.value) {
    done.value = true
    return
  }
  current.value++
  answer.value  = ''
  revealed.value = false
  inputState.value = ''
  nextTick(() => inputEl.value?.focus())
}

function restart() {
  current.value = 0
  answer.value  = ''
  revealed.value = false
  inputState.value = ''
  score.value   = 0
  done.value    = false
  nextTick(() => inputEl.value?.focus())
}
</script>

<style scoped>
.exercise-progress {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 2rem;
}

.progress-bar {
  flex: 1;
  height: 0.5rem;
  background-color: var(--gray-200, #e2e8f0);
  border-radius: 999px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background-color: var(--teal-500, #14b8a6);
  transition: width 0.3s ease;
}

.progress-label {
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--gray-600, #475569);
}

.result-card, .exercise-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2rem;
  background: white;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.result-score {
  font-size: 3rem;
  font-weight: bold;
  color: var(--teal-600, #0d9488);
  margin: 0;
}

.result-label {
  font-size: 1.25rem;
  color: var(--gray-500, #64748b);
  margin-bottom: 1.5rem;
}

.exercise-prompt-label {
  font-size: 0.875rem;
  color: var(--gray-500, #64748b);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 0.5rem;
}

.exercise-prompt {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 2rem;
}

.exercise-input-row {
  display: flex;
  gap: 0.5rem;
  width: 100%;
  max-width: 400px;
}

.exercise-input {
  flex: 1;
  padding: 0.75rem 1rem;
  border: 1px solid var(--gray-300, #cbd5e1);
  border-radius: 0.375rem;
  font-size: 1rem;
}

.exercise-input.correct {
  border-color: var(--green-500, #22c55e);
  background-color: var(--green-50, #f0fdf4);
}

.exercise-input.wrong {
  border-color: var(--red-500, #ef4444);
  background-color: var(--red-50, #fef2f2);
}

.feedback {
  margin-top: 1.5rem;
  font-size: 1.125rem;
  font-weight: 500;
}

.feedback.correct {
  color: var(--green-600, #16a34a);
}

.feedback.wrong {
  color: var(--red-600, #dc2626);
}
</style>