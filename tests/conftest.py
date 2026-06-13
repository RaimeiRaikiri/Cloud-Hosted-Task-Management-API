from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db
from app.database_models import Base
import app.database_models as database_models
import pytest
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.models import UserCreate
from fastapi import Depends

import os
from dotenv import load_dotenv

load_dotenv()

postgres_password = os.getenv("postgres_password")
SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:{postgres_password}@localhost:5432/taskdb_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
Testing_Session_Local = sessionmaker(bind=engine)

def override_get_db():
    db = Testing_Session_Local()
    try: 
        yield db
    finally:
        db.close()
        
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def test_client():
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    Base.metadata.drop_all(bind=engine)
    
@pytest.fixture
def user(test_client: TestClient):
    response = test_client.post("/users", json={
        "username":"test",
        "email":"test@gmail.com",
        "password":"password"
    })

    return response.json()

@pytest.fixture
def token(test_client: TestClient, user):
    response = test_client.post(
        "/auth/token",
        data="username=test&password=password",
        headers={
            "content-type":"application/x-www-form-urlencoded"
            }
        )
    
    return response.json()["access_token"]