import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from backend.main import app, get_session
from backend.models import User, Room
from backend.auth import get_password_hash

@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", 
        connect_args={"check_same_thread": False}, 
        poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session
    
    app.dependency_overrides[get_session] = get_session_override
    
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

def test_create_room(client: TestClient):
    # First create a user
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass"
    }
    response = client.post("/register", json=user_data)
    assert response.status_code == 200
    
    # Login to get token
    login_data = {
        "username": "testuser",
        "password": "testpass"
    }
    response = client.post("/token", json=login_data)
    assert response.status_code == 200
    token = response.json()["access_token"]
    
    # Create a room
    room_data = {
        "name": "Test Room",
        "description": "A test room",
        "is_public": True
    }
    response = client.post(
        "/rooms", 
        json=room_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Room"
    assert data["description"] == "A test room"
    assert data["is_public"] == True

def test_get_rooms(client: TestClient):
    # Create user and login (similar to above test)
    user_data = {
        "username": "testuser2",
        "email": "test2@example.com",
        "password": "testpass"
    }
    client.post("/register", json=user_data)
    
    login_data = {
        "username": "testuser2",
        "password": "testpass"
    }
    response = client.post("/token", json=login_data)
    token = response.json()["access_token"]
    
    # Create a room
    room_data = {
        "name": "Test Room 2",
        "description": "Another test room",
        "is_public": True
    }
    client.post(
        "/rooms", 
        json=room_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    
    # Get rooms
    response = client.get(
        "/rooms",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Test Room 2"