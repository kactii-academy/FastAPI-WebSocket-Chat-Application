from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Remove this if it causes issues:
    # messages: List["Message"] = Relationship(back_populates="user")

class Room(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_public: bool = Field(default=True)
    
    # Remove this if it causes issues:
    # messages: List["Message"] = Relationship(back_populates="room")

class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    user_id: int = Field(foreign_key="user.id")
    room_id: int = Field(foreign_key="room.id")
    
    # Remove these if they cause issues:
    # user: User = Relationship(back_populates="messages")
    # room: Room = Relationship(back_populates="messages")