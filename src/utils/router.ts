import { createRouter, createWebHashHistory } from 'vue-router'

import Home from '@/views/Home.vue'
import HomePage from '@/views/homePage/index.vue'
import Recommend from '@/views/recommend/index.vue'
import UserPage from '@/views/userPage/index.vue'
import CategoryPage from '@/views/categoryPage/index.vue'

const routes = [
  {
    path: '/',
    component: Home,
    children: [
      { path: '', component: Recommend },
      { path: 'home/:hot', component: HomePage },
      { path: 'my', component: UserPage },
      { path: 'category/:category', component: CategoryPage },
    ],
  },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes,
})

export default router
