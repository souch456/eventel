import { createRouter, createWebHistory } from 'vue-router'
import EventsMapView from '../views/EventsMapView.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: EventsMapView,
  },
  // 追加のページがあればここに追記
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
