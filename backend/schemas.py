from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True

class RoomCreate(BaseModel):
    name: str
    description: Optional[str] = None
    is_public: bool = True

class RoomResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    created_at: datetime
    is_public: bool

    class Config:
        from_attributes = True

class MessageCreate(BaseModel):
    content: str
    room_id: int

class MessageResponse(BaseModel):
    id: int
    content: str
    timestamp: datetime
    user_id: int
    room_id: int
    username: str

    class Config:
        from_attributes = True