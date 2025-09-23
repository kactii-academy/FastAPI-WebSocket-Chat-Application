<template>
  <div class="chat-room-container">
    <div class="chat-header">
      <h2>{{ room.name }}</h2>
      <p>{{ room.description }}</p>
      <div class="online-users">
        <span>Online: {{ onlineUsers.length }}</span>
      </div>
    </div>
    
    <div class="chat-messages" ref="messagesContainer">
      <div v-for="message in messages" :key="message.id" class="message">
        <div class="message-header">
          <strong>{{ message.username }}</strong>
          <span class="timestamp">{{ formatTimestamp(message.timestamp) }}</span>
        </div>
        <div class="message-content">{{ message.content }}</div>
      </div>
    </div>
    
    <div class="chat-input">
      <form @submit.prevent="sendMessage">
        <input
          v-model="newMessage"
          type="text"
          placeholder="Type your message..."
          :disabled="!isConnected"
        />
        <button type="submit" :disabled="!newMessage || !isConnected">
          Send
        </button>
      </form>
    </div>
    
    <div v-if="!isConnected" class="connection-status">
      <p>Connecting to chat...</p>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import { useAuthStore } from '../stores/auth'

export default {
  name: 'ChatRoom',
  props: {
    roomId: {
      type: String,
      required: true
    }
  },
  setup(props) {
    const authStore = useAuthStore()
    const route = useRoute()
    
    const room = ref({})
    const messages = ref([])
    const newMessage = ref('')
    const ws = ref(null)
    const isConnected = ref(false)
    const onlineUsers = ref([])
    const messagesContainer = ref(null)
    
    const connectWebSocket = () => {
      const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
      const wsUrl = `${protocol}//${window.location.host}/ws/${props.roomId}?token=${authStore.token}`
      
      ws.value = new WebSocket(wsUrl)
      
      ws.value.onopen = () => {
        isConnected.value = true
        console.log('WebSocket connected')
      }
      
      ws.value.onmessage = (event) => {
        const data = JSON.parse(event.data)
        
        if (data.type === 'message') {
          messages.value.push({
            id: Date.now() + Math.random(),
            content: data.content,
            username: data.username,
            timestamp: data.timestamp
          })
          scrollToBottom()
        } else if (data.type === 'user_joined') {
          onlineUsers.value.push(data.user_id)
          messages.value.push({
            id: Date.now() + Math.random(),
            content: data.message,
            username: 'System',
            timestamp: new Date().toISOString()
          })
        } else if (data.type === 'user_left') {
          onlineUsers.value = onlineUsers.value.filter(user => user !== data.user_id)
          messages.value.push({
            id: Date.now() + Math.random(),
            content: data.message,
            username: 'System',
            timestamp: new Date().toISOString()
          })
        }
      }
      
      ws.value.onclose = () => {
        isConnected.value = false
        console.log('WebSocket disconnected')
        // Try to reconnect after 3 seconds
        setTimeout(connectWebSocket, 3000)
      }
      
      ws.value.onerror = (error) => {
        console.error('WebSocket error:', error)
        isConnected.value = false
      }
    }
    
    const fetchRoomDetails = async () => {
      try {
        const response = await axios.get(`http://localhost:8000/rooms/${props.roomId}`, {
          headers: {
            'Authorization': `Bearer ${authStore.token}`
          }
        })
        room.value = response.data
      } catch (error) {
        console.error('Failed to fetch room details:', error)
      }
    }
    
    const fetchMessages = async () => {
      try {
        const response = await axios.get(`http://localhost:8000/rooms/${props.roomId}/messages`, {
          headers: {
            'Authorization': `Bearer ${authStore.token}`
          }
        })
        messages.value = response.data
        scrollToBottom()
      } catch (error) {
        console.error('Failed to fetch messages:', error)
      }
    }
    
    const sendMessage = () => {
      if (newMessage.value.trim() && ws.value && isConnected.value) {
        const messageData = {
          content: newMessage.value.trim(),
          type: 'message'
        }
        ws.value.send(JSON.stringify(messageData))
        newMessage.value = ''
      }
    }
    
    const scrollToBottom = () => {
      nextTick(() => {
        if (messagesContainer.value) {
          messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
        }
      })
    }
    
    const formatTimestamp = (timestamp) => {
      return new Date(timestamp).toLocaleTimeString()
    }
    
    onMounted(() => {
      fetchRoomDetails()
      fetchMessages()
      connectWebSocket()
    })
    
    onUnmounted(() => {
      if (ws.value) {
        ws.value.close()
      }
    })
    
    watch(() => props.roomId, (newRoomId) => {
      if (ws.value) {
        ws.value.close()
      }
      messages.value = []
      fetchRoomDetails()
      fetchMessages()
      connectWebSocket()
    })
    
    return {
      room,
      messages,
      newMessage,
      isConnected,
      onlineUsers,
      messagesContainer,
      sendMessage,
      formatTimestamp
    }
  }
}
</script>

<style scoped>
.chat-room-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  max-width: 1000px;
  margin: 0 auto;
}

.chat-header {
  background: white;
  padding: 1rem;
  border-bottom: 1px solid #eee;
  text-align: center;
}

.chat-header h2 {
  margin: 0 0 0.5rem 0;
  color: #333;
}

.chat-header p {
  margin: 0 0 1rem 0;
  color: #666;
}

.online-users {
  color: #4CAF50;
  font-weight: 500;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
  background-color: #f9f9f9;
}

.message {
  background: white;
  padding: 0.75rem;
  margin-bottom: 1rem;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.message-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.message-header strong {
  color: #333;
}

.timestamp {
  color: #999;
  font-size: 0.8rem;
}

.message-content {
  color: #333;
}

.chat-input {
  background: white;
  padding: 1rem;
  border-top: 1px solid #eee;
}

.chat-input form {
  display: flex;
  gap: 0.5rem;
}

.chat-input input {
  flex: 1;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.chat-input button {
  padding: 0.75rem 1.5rem;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
}

.chat-input button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.connection-status {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  background-color: #fff3cd;
  color: #856404;
  padding: 0.5rem;
  text-align: center;
  border-bottom: 1px solid #ffeaa7;
}
</style>