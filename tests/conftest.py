import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import get_db, Base
from app.models import User

from sqlalchemy.pool import StaticPool

DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool  # Ensures the same connection is reused
)
# #DATABASE_URL = "sqlite:///test.db"
# DATABASE_URL = "sqlite:///:memory:"
# engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    try:
        seed_data(db)
        db.commit()
    finally:
        db.close()

    test_client = TestClient(app)
    yield test_client

    Base.metadata.drop_all(bind=engine)

def seed_data(db):
    users = [
        User(username="user1", email="user1@example.com"),
        User(username="user2", email="user2@example.com"),
        User(username="user3", email="user3@example.com"),
    ]

    db.add_all(users)
