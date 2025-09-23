from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session
from typing import List
from datetime import datetime, timedelta
import json

from .database import init_db, get_session
from .models import User, Room, Message
from .schemas import UserCreate, UserResponse, RoomCreate, RoomResponse, MessageCreate, MessageResponse, Token
from .auth import authenticate_user, create_access_token, get_password_hash, get_current_user
from .manager import manager
from .crud import create_user, get_user_by_username, get_rooms, create_room, get_room, create_message, get_messages
from .config import settings

# Create app first
app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
@app.on_event("startup")
def on_startup():
    init_db()

# Auth endpoints
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: dict, session: Session = Depends(get_session)):
    user = authenticate_user(form_data["username"], form_data["password"], session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate, session: Session = Depends(get_session)):
    from .auth import get_password_hash  # Import here to avoid circular imports
    
    db_user = get_user_by_username(session, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = get_password_hash(user.password)
    new_user = create_user(session, user, hashed_password)
    return new_user

# Room endpoints
@app.get("/rooms", response_model=List[RoomResponse])
async def read_rooms(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    rooms = get_rooms(session, skip=skip, limit=limit)
    return rooms

@app.post("/rooms", response_model=RoomResponse)
async def create_new_room(room: RoomCreate, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    new_room = create_room(session, room)
    return new_room

@app.get("/rooms/{room_id}")
async def get_room_by_id(room_id: int, session: Session = Depends(get_session)):
    room = get_room(session, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room

# Message endpoints
@app.get("/rooms/{room_id}/messages", response_model=List[MessageResponse])
async def read_messages(room_id: int, skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    messages = get_messages(session, room_id, skip=skip, limit=limit)
    return messages

# WebSocket endpoint
@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str, token: str = None):
    if not token:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    
    try:
        # Verify token and get user
        session = next(get_session())
        user = await get_current_user(token, session)
        
        # Connect to the room
        await manager.connect(websocket, room_id, user.username)
        
        try:
            while True:
                data = await websocket.receive_text()
                message_data = json.loads(data)
                
                # Save message to database
                message_create = MessageCreate(
                    content=message_data["content"],
                    room_id=int(room_id)
                )
                create_message(session, message_create, user.id)
                
                # Prepare message for broadcasting
                broadcast_message = {
                    "type": "message",
                    "content": message_data["content"],
                    "user_id": user.id,
                    "username": user.username,
                    "timestamp": str(datetime.utcnow())
                }
                
                # Broadcast to all users in the room
                await manager.broadcast_to_room(
                    room_id, 
                    json.dumps(broadcast_message),
                    exclude_user=user.username
                )
                
        except WebSocketDisconnect:
            manager.disconnect(room_id, user.username)
            
    except HTTPException:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    except Exception as e:
        print(f"WebSocket error: {e}")
        await websocket.close(code=status.WS_1011_INTERNAL_ERROR)
        return

# Root endpoint
@app.get("/")
async def root():
    return {"message": "FastAPI WebSocket Chat Application", "endpoints": {
        "documentation": "/docs",
        "websocket": "/ws/{room_id}",
        "rooms": "/rooms",
        "messages": "/rooms/{room_id}/messages"
    }}

# Add security scheme to OpenAPI
@app.on_event("startup")
async def set_up_openapi():
    openapi_schema = app.openapi()
    
    # Ensure components exist
    if "components" not in openapi_schema:
        openapi_schema["components"] = {}
    
    # Add security schemes
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    
    # Add security requirements
    if "security" not in openapi_schema:
        openapi_schema["security"] = []
    
    app.openapi_schema = openapi_schema

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)