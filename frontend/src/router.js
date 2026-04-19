import { createRouter, createWebHistory } from 'vue-router'
import DailyStudy from './views/DailyStudy.vue'
import History    from './views/History.vue'
import Review     from './views/Review.vue'

const routes = [
  { path: '/',              component: DailyStudy },
  { path: '/history',       component: History    },
  { path: '/review/:id',    component: Review     },
]

export const router = createRouter({
  history: createWebHistory(),
  routes,
})
