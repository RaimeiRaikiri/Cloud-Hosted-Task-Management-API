from fastapi.testclient import TestClient
from app.main import app
import pytest

@pytest.fixture
def test_client():
    with TestClient(app) as client:
        yield client