from sqlmodel import Session, select
from .models import User, Room, Message
from .schemas import UserCreate, RoomCreate, MessageCreate

def create_user(session: Session, user: UserCreate, hashed_password: str):
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

def get_user_by_username(session: Session, username: str):
    return session.exec(select(User).where(User.username == username)).first()

def get_rooms(session: Session, skip: int = 0, limit: int = 100):
    return session.exec(select(Room).offset(skip).limit(limit)).all()

def create_room(session: Session, room: RoomCreate):
    db_room = Room(
        name=room.name,
        description=room.description,
        is_public=room.is_public
    )
    session.add(db_room)
    session.commit()
    session.refresh(db_room)
    return db_room

def get_room(session: Session, room_id: int):
    return session.exec(select(Room).where(Room.id == room_id)).first()

def create_message(session: Session, message: MessageCreate, user_id: int):
    db_message = Message(
        content=message.content,
        user_id=user_id,
        room_id=message.room_id
    )
    session.add(db_message)
    session.commit()
    session.refresh(db_message)
    return db_message

def get_messages(session: Session, room_id: int, skip: int = 0, limit: int = 100):
    return session.exec(
        select(Message)
        .where(Message.room_id == room_id)
        .order_by(Message.timestamp.desc())
        .offset(skip)
        .limit(limit)
    ).all()