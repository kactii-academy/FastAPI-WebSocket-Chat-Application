import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

import LoginForm from '../components/LoginForm.vue'
import RoomList from '../components/RoomList.vue'
import ChatRoom from '../components/ChatRoom.vue'

const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginForm
  },
  {
    path: '/rooms',
    name: 'Rooms',
    component: RoomList,
    meta: { requiresAuth: true }
  },
  {
    path: '/chat/:roomId',
    name: 'ChatRoom',
    component: ChatRoom,
    meta: { requiresAuth: true },
    props: true
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
  } else {
    next()
  }
})

export default router