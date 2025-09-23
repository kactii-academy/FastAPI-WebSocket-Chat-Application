from sqlmodel import SQLModel, create_engine, Session
from .config import settings

# For SQLite, we need to add connect_args
engine = create_engine(
    settings.DATABASE_URL, 
    echo=True,
    connect_args={"check_same_thread": False}  # Needed for SQLite
)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session