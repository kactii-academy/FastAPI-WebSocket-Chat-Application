from fastapi import Depends, HTTPException, status
from sqlmodel import Session
from .database import get_session
from .auth import get_current_user
from .models import User

def get_db():
    return Depends(get_session)

def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user