from fastapi import status
from fastapi.testclient import TestClient
from test_tasks import auth_headers

BASEURL = "/auth"


def test_access_token_authorized(test_client: TestClient, user):
    response = test_client.post(
        f"{BASEURL}/token",
        data="username=test&password=password",
        headers={"content-type": "application/x-www-form-urlencoded"},
    )

    json_response = response.json()

    assert isinstance(json_response["access_token"], str) and isinstance(
        json_response["token_type"], str
    )

    assert response.status_code == status.HTTP_200_OK


def test_access_token_unauthorized(test_client: TestClient):
    response = test_client.post(
        f"{BASEURL}/token",
        data="username=wrong&password=wrong",
        headers={"content-type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_create_user(test_client: TestClient):
    response = test_client.post(
        "/users",
        json={
            "username": "create_user_test",
            "email": "mikescutts10@gmail.com",
            "password": "password",
        },
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["username"] == "create_user_test"


def test_create_user_conflict_username(test_client: TestClient, user):
    response = test_client.post(
        "/users",
        json={"username": "test", "email": "testing@gmail.com", "password": "password"},
    )

    assert response.status_code == status.HTTP_409_CONFLICT


def test_create_user_conflict_email(test_client: TestClient, user):
    response = test_client.post(
        "/users",
        json={
            "username": "create_user_test",
            "email": "test@gmail.com",
            "password": "password",
        },
    )

    assert response.status_code == status.HTTP_409_CONFLICT


def test_get_user(test_client: TestClient, user, token):
    response = test_client.get("/users/me", headers=auth_headers(token))

    assert response.status_code == status.HTTP_200_OK

    response_json = response.json()
    assert response_json["username"] == "test"


def test_get_user_unauthorised(test_client: TestClient, user):
    response = test_client.get("/users/me")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
