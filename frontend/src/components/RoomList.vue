<template>
  <div class="room-list-container">
    <div class="header">
      <h2>Chat Rooms</h2>
      <button @click="showCreateRoomModal = true" class="create-room-btn">
        Create Room
      </button>
    </div>
    
    <div class="rooms-grid">
      <div 
        v-for="room in rooms" 
        :key="room.id" 
        class="room-card"
        @click="joinRoom(room)"
      >
        <h3>{{ room.name }}</h3>
        <p>{{ room.description || 'No description' }}</p>
        <div class="room-meta">
          <span class="public-badge" v-if="room.is_public">Public</span>
          <span class="private-badge" v-else>Private</span>
        </div>
      </div>
    </div>
    
    <div v-if="rooms.length === 0" class="empty-state">
      <p>No rooms available. Create the first one!</p>
    </div>
    
    <!-- Create Room Modal -->
    <div v-if="showCreateRoomModal" class="modal-overlay" @click.self="showCreateRoomModal = false">
      <div class="modal-content">
        <h3>Create New Room</h3>
        <form @submit.prevent="createRoom">
          <div class="form-group">
            <label for="roomName">Room Name</label>
            <input
              id="roomName"
              v-model="newRoom.name"
              type="text"
              required
              placeholder="Enter room name"
            />
          </div>
          
          <div class="form-group">
            <label for="roomDescription">Description</label>
            <textarea
              id="roomDescription"
              v-model="newRoom.description"
              placeholder="Enter room description (optional)"
              rows="3"
            ></textarea>
          </div>
          
          <div class="form-group">
            <label class="checkbox-label">
              <input
                type="checkbox"
                v-model="newRoom.is_public"
              />
              Public Room
            </label>
          </div>
          
          <div class="modal-actions">
            <button type="button" @click="showCreateRoomModal = false">
              Cancel
            </button>
            <button type="submit" :disabled="creatingRoom">
              {{ creatingRoom ? 'Creating...' : 'Create Room' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { useAuthStore } from '../stores/auth'

export default {
  name: 'RoomList',
  setup() {
    const authStore = useAuthStore()
    const router = useRouter()
    
    const rooms = ref([])
    const showCreateRoomModal = ref(false)
    const creatingRoom = ref(false)
    
    const newRoom = ref({
      name: '',
      description: '',
      is_public: true
    })
    
    const fetchRooms = async () => {
      try {
        const response = await axios.get('http://localhost:8000/rooms', {
          headers: {
            'Authorization': `Bearer ${authStore.token}`
          }
        })
        rooms.value = response.data
      } catch (error) {
        console.error('Failed to fetch rooms:', error)
      }
    }
    
    const createRoom = async () => {
      creatingRoom.value = true
      try {
        const response = await axios.post('http://localhost:8000/rooms', newRoom.value, {
          headers: {
            'Authorization': `Bearer ${authStore.token}`
          }
        })
        
        rooms.value.push(response.data)
        showCreateRoomModal.value = false
        newRoom.value = { name: '', description: '', is_public: true }
      } catch (error) {
        console.error('Failed to create room:', error)
      } finally {
        creatingRoom.value = false
      }
    }
    
    const joinRoom = (room) => {
      router.push({ name: 'ChatRoom', params: { roomId: room.id } })
    }
    
    onMounted(() => {
      fetchRooms()
    })
    
    return {
      rooms,
      showCreateRoomModal,
      creatingRoom,
      newRoom,
      createRoom,
      joinRoom
    }
  }
}
</script>

<style scoped>
.room-list-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 2rem;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.create-room-btn {
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
}

.rooms-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.room-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.room-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.room-card h3 {
  margin: 0 0 0.5rem 0;
  color: #333;
}

.room-card p {
  color: #666;
  margin: 0 0 1rem 0;
}

.room-meta {
  display: flex;
  gap: 0.5rem;
}

.public-badge, .private-badge {
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 500;
}

.public-badge {
  background-color: #e8f5e8;
  color: #2e7d32;
}

.private-badge {
  background-color: #fff3e0;
  color: #f57c00;
}

.empty-state {
  text-align: center;
  padding: 3rem;
  color: #666;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  width: 90%;
  max-width: 500px;
}

.modal-content h3 {
  margin-top: 0;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 1.5rem;
}

.modal-actions button {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.modal-actions button[type="button"] {
  background-color: #f5f5f5;
  color: #333;
}

.modal-actions button[type="submit"] {
  background-color: #4CAF50;
  color: white;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}
</style>