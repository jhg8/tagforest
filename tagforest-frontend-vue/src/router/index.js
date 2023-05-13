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
        component: () => import(/* webpackChunkName: "category" */ '../views/CategoryView.vue')
      },
      {
        path: 'tag/:tagid',
        name: 'tag',
        component: () => import(/* webpackChunkName: "tag" */ '../views/TagDetailView.vue')
      },
    ],
  },
  {
    path: '/',
    name: 'welcome',
    component: () => import(/* webpackChunkName: "welcome" */ '../views/WelcomeView.vue')
  },
  {
    path: '/register',
    name: 'register',
    component: () => import(/* webpackChunkName: "register" */ '../views/RegisterView.vue')
  },
  {
    path: '/public/tree/:id',
    name: 'publictree',
    component: () => import(/* webpackChunkName: "publictree" */ '../views/PublicGraph.vue')
  },
  {
    path: '/public/tree/:treeId/tag/:id',
    name: 'publictag',
    component: () => import(/* webpackChunkName: "publictag" */ '../views/PublicTag.vue')
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
