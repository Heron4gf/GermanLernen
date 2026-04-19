<template>
  <div>

    <header class="app-header">
      <div class="container header-inner">
        <router-link to="/" class="logo" aria-label="GermanLernen home">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" aria-hidden="true">
            <rect x="3" y="3" width="18" height="18" rx="3" stroke="currentColor" stroke-width="1.5"/>
            <path d="M7 8h5M7 12h8M7 16h5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          </svg>
          GermanLernen
        </router-link>

        <nav class="nav" aria-label="Main navigation">
          <router-link to="/" class="nav-link" exact-active-class="active">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
            <span>Today</span>
          </router-link>
          <router-link to="/history" class="nav-link" active-class="active">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M12 8v4l3 3"/><circle cx="12" cy="12" r="9"/></svg>
            <span>History</span>
          </router-link>

          <button
            class="theme-toggle"
            data-theme-toggle
            aria-label="Toggle theme"
            style="margin-left:var(--space-2)"
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>
          </button>
        </nav>
      </div>
    </header>

    <div id="main-content">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'

onMounted(() => {
  const toggle = document.querySelector('[data-theme-toggle]')
  const root   = document.documentElement
  let theme    = matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
  root.setAttribute('data-theme', theme)

  const sunIcon  = `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>`
  const moonIcon = `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>`

  toggle?.addEventListener('click', () => {
    theme = theme === 'dark' ? 'light' : 'dark'
    root.setAttribute('data-theme', theme)
    toggle.innerHTML = theme === 'dark' ? sunIcon : moonIcon
  })
})
</script>
