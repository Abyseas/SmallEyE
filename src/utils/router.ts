import { createRouter, createWebHashHistory } from 'vue-router'

import Home from '@/views/Home.vue'
import Recommend from '@/views/recommend/index.vue'

const routes = [
  {
    path: '/',
    component: Home,
    children: [{ path: '', component: Recommend }],
  },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes,
})

export default router
