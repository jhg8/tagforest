import { createRouter, createWebHistory } from 'vue-router'
import GraphView from '../views/GraphView.vue'

const routes = [
  {
    path: '/',
    name: 'Graph View',
    component: GraphView
  },
  {
    path: '/tag/:id',
    name: 'Tag',
    component: () => import(/* webpackChunkName: "tag" */ '../views/TagDetailView.vue')
  },
  {
    path: '/auth',
    name: 'AuthView',
    component: () => import(/* webpackChunkName: "auth" */ '../views/AuthView.vue')
  },
  {
    path: '/about',
    name: 'About',
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import(/* webpackChunkName: "profile" */ '../views/Profile.vue')
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
