<template>
  <div class="login-container">
    <div class="login-form">
      <h2>{{ isRegistering ? 'Register' : 'Login' }}</h2>
      
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label for="username">Username</label>
          <input
            id="username"
            v-model="form.username"
            type="text"
            required
            placeholder="Enter your username"
          />
        </div>
        
        <div v-if="isRegistering" class="form-group">
          <label for="email">Email</label>
          <input
            id="email"
            v-model="form.email"
            type="email"
            required
            placeholder="Enter your email"
          />
        </div>
        
        <div class="form-group">
          <label for="password">Password</label>
          <input
            id="password"
            v-model="form.password"
            type="password"
            required
            placeholder="Enter your password"
          />
        </div>
        
        <button type="submit" :disabled="loading">
          {{ loading ? 'Processing...' : isRegistering ? 'Register' : 'Login' }}
        </button>
      </form>
      
      <p class="toggle-mode">
        {{ isRegistering ? 'Already have an account?' : "Don't have an account?" }}
        <a href="#" @click.prevent="toggleMode">
          {{ isRegistering ? 'Login' : 'Register' }}
        </a>
      </p>
      
      <div v-if="error" class="error-message">
        {{ error }}
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

export default {
  name: 'LoginForm',
  setup() {
    const authStore = useAuthStore()
    const router = useRouter()
    
    const isRegistering = ref(false)
    const loading = ref(false)
    const error = ref('')
    
    const form = reactive({
      username: '',
      email: '',
      password: ''
    })
    
    const toggleMode = () => {
      isRegistering.value = !isRegistering.value
      error.value = ''
    }
    
    const handleSubmit = async () => {
      loading.value = true
      error.value = ''
      
      try {
        let result
        if (isRegistering.value) {
          result = await authStore.register(form.username, form.email, form.password)
        } else {
          result = await authStore.login(form.username, form.password)
        }
        
        if (result.success) {
          router.push('/rooms')
        } else {
          error.value = result.error
        }
      } catch (err) {
        error.value = 'An unexpected error occurred'
      } finally {
        loading.value = false
      }
    }
    
    return {
      isRegistering,
      loading,
      error,
      form,
      toggleMode,
      handleSubmit
    }
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f5f5;
}

.login-form {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

h2 {
  text-align: center;
  margin-bottom: 1.5rem;
  color: #333;
}

.form-group {
  margin-bottom: 1rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  color: #555;
}

input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

button {
  width: 100%;
  padding: 0.75rem;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  margin-top: 1rem;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.toggle-mode {
  text-align: center;
  margin-top: 1rem;
  color: #666;
}

a {
  color: #4CAF50;
  text-decoration: none;
}

.error-message {
  color: #f44336;
  text-align: center;
  margin-top: 1rem;
  padding: 0.5rem;
  background-color: #ffebee;
  border-radius: 4px;
}
</style>