import { createRouter, createWebHistory } from 'vue-router'
import RootTreeView from '../views/RootTreeView.vue'
import GraphView from '../views/GraphView.vue'

const routes = [
  {
    path: '/trees/:id?',
    component: RootTreeView,
    children: [
      {
        path: 'graph',
        name: 'graph',
        component: GraphView,
        alias: ''
      },
      {
        path: 'category',
        name: 'category',
        component: () => import(/* webpackChunkName: "tag" */ '../views/CategoryView.vue')
      },
      {
        path: 'tag/:tagid',
        name: 'tag',
        component: () => import(/* webpackChunkName: "tag" */ '../views/TagDetailView.vue')
      },
    ],
    alias: '/'
  },
  {
    path: '/auth',
    name: 'auth',
    component: () => import(/* webpackChunkName: "auth" */ '../views/AuthView.vue')
  },
  {
    path: '/about',
    name: 'about',
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  },
  {
    path: '/profile',
    name: 'profile',
    component: () => import(/* webpackChunkName: "profile" */ '../views/Profile.vue')
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
