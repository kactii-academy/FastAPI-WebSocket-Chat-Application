from fastapi import WebSocket, status
from typing import Dict, List
import json

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, Dict[str, WebSocket]] = {}
        # Structure: {room_id: {user_id: websocket}}

    async def connect(self, websocket: WebSocket, room_id: str, user_id: str):
        await websocket.accept()
        if room_id not in self.active_connections:
            self.active_connections[room_id] = {}
        self.active_connections[room_id][user_id] = websocket
        
        # Notify room that user joined
        join_message = {
            "type": "user_joined",
            "user_id": user_id,
            "message": f"User {user_id} joined the room"
        }
        await self.broadcast_to_room(room_id, json.dumps(join_message), exclude_user=user_id)

    def disconnect(self, room_id: str, user_id: str):
        if room_id in self.active_connections and user_id in self.active_connections[room_id]:
            del self.active_connections[room_id][user_id]
            
            # Notify room that user left
            leave_message = {
                "type": "user_left",
                "user_id": user_id,
                "message": f"User {user_id} left the room"
            }
            # We can't await here, so we'd need to handle this differently
            # For simplicity, we'll just remove the user

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast_to_room(self, room_id: str, message: str, exclude_user: str = None):
        if room_id in self.active_connections:
            for user_id, connection in self.active_connections[room_id].items():
                if user_id != exclude_user:
                    await connection.send_text(message)

    def get_online_users(self, room_id: str):
        if room_id in self.active_connections:
            return list(self.active_connections[room_id].keys())
        return []

# Create a single instance of our manager
manager = ConnectionManager()