<template>
  <div id="app">
    <nav>
      <router-link to="/">Home</router-link> |
      <router-link to="/login" v-if="!authStore.isAuthenticated">Login</router-link>
      <span v-else>
        <router-link to="/chat">Chat</router-link> |
        <button @click="authStore.logout">Logout</button>
      </span>
    </nav>
    <router-view/>
  </div>
</template>

<script>
import { useAuthStore } from './stores/auth'

export default {
  name: 'App',
  setup() {
    const authStore = useAuthStore()
    return { authStore }
  }
}
</script>