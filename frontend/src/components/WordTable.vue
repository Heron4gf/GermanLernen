<template>
  <table class="word-table" aria-label="Vocabulary list">
    <thead>
      <tr>
        <th>Deutsch</th>
        <th>English</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="word in words" :key="word.word">
        <td class="word-de">{{ word.word }}</td>
        <td class="word-en">{{ word.translation }}</td>
      </tr>
    </tbody>
  </table>
</template>

<script setup>
defineProps({ words: { type: Array, required: true } })
</script>
