<template>
  <div>
    <div class="exercise-progress">
      <div class="progress-bar" role="progressbar" :aria-valuenow="current + 1" :aria-valuemax="words.length">
        <div class="progress-fill" :style="{ width: progressPct + '%' }"></div>
      </div>
      <span class="progress-label">{{ current + 1 }}/{{ words.length }}</span>
    </div>

    <!-- Result screen -->
    <transition name="fade">
      <div v-if="done" class="card result-card">
        <p class="result-score">{{ score }}/{{ words.length }}</p>
        <p class="result-label">correct answers</p>
        <button class="btn btn-primary btn-lg" @click="restart">Try again</button>
      </div>
    </transition>

    <!-- Exercise card -->
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
const inputState = ref('')   // '' | 'correct' | 'wrong'
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
