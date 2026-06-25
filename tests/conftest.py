import os
from datetime import datetime, timezone

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import app.database_models as database_models
from app.database import get_db
from app.database_models import Base
from app.main import app
from app.routers.auth import get_password_hash

load_dotenv()

TEST_DB_URL = os.getenv("TEST_DATABASE_URL")


engine = create_engine(TEST_DB_URL)
Testing_Session_Local = sessionmaker(bind=engine)


def override_get_db():
    db = Testing_Session_Local()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def db():
    session = Testing_Session_Local()
    yield session
    session.close()


@pytest.fixture
def test_client():
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def user(test_client: TestClient, db):
    test_user = database_models.User(
        username="test", email="test@gmail.com", password=get_password_hash("password")
    )

    db.add(test_user)
    db.commit()
    db.refresh(test_user)

    return test_user


@pytest.fixture
def second_user(test_client: TestClient, db):
    test_user = database_models.User(
        username="testtwo",
        email="testtwo@gmail.com",
        password=get_password_hash("password"),
    )

    db.add(test_user)
    db.commit()
    db.refresh(test_user)

    return test_user


@pytest.fixture
def token(test_client: TestClient, user):
    response = test_client.post(
        "/auth/token",
        data="username=test&password=password",
        headers={"content-type": "application/x-www-form-urlencoded"},
    )

    return response.json()["access_token"]


@pytest.fixture
def task(test_client: TestClient, user, db):
    test_task = database_models.Task(
        title="test",
        description="task tester",
        completed=False,
        user_id=user.id,
        created_at=datetime.now(timezone.utc),
    )

    db.add(test_task)
    db.commit()
    db.refresh(test_task)

    return test_task


@pytest.fixture
def second_user_task(test_client: TestClient, second_user, db):
    test_task = database_models.Task(
        title="testing",
        description="task tester for user 2!",
        completed=False,
        user_id=second_user.id,
        created_at=datetime.now(timezone.utc),
    )

    db.add(test_task)
    db.commit()
    db.refresh(test_task)

    return test_task
