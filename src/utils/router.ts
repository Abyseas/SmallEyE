import { createRouter, createWebHashHistory } from 'vue-router'

import Home from '@/views/Home.vue'
import HomePage from '@/views/homepage/index.vue'
import Recommend from '@/views/recommend/index.vue'

const routes = [
  {
    path: '/',
    component: Home,
    children: [
      { path: '', component: Recommend },
      { path: 'home', component: HomePage },
    ],
  },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes,
})

export default router
