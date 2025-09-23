import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token'))
  const user = ref(JSON.parse(localStorage.getItem('user') || 'null'))
  const isAuthenticated = ref(!!token.value)

  const API_BASE = 'http://localhost:8000'

  const login = async (username, password) => {
    try {
      const response = await axios.post(`${API_BASE}/token`, {
        username,
        password
      })
      
      token.value = response.data.access_token
      user.value = { username }
      isAuthenticated.value = true
      
      localStorage.setItem('token', token.value)
      localStorage.setItem('user', JSON.stringify(user.value))
      
      return { success: true }
    } catch (error) {
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Login failed' 
      }
    }
  }

  const register = async (username, email, password) => {
    try {
      const response = await axios.post(`${API_BASE}/register`, {
        username,
        email,
        password
      })
      
      // After registration, automatically log in
      return await login(username, password)
    } catch (error) {
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Registration failed' 
      }
    }
  }

  const logout = () => {
    token.value = null
    user.value = null
    isAuthenticated.value = false
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  return {
    token,
    user,
    isAuthenticated,
    login,
    register,
    logout
  }
})