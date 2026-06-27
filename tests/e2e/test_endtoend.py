from fastapi import status
from fastapi.testclient import TestClient


def auth_headers(token):

    return {"Authorization": f"Bearer {token}"}


def test_user_CRUD_lifecycle(test_client: TestClient):
    # Create user
    response = test_client.post(
        "/users/",
        json={"username": "Jake", "email": "mikescutts10@gmail.com", "password": "password"},
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {"username": "Jake"}

    # Login/Get JWT

    response = test_client.post(
        "/auth/token",
        data="username=Jake&password=password",
        headers={"content-type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == status.HTTP_200_OK

    jwt = response.json()
    token = jwt["access_token"]

    assert (
        isinstance(jwt, dict)
        and isinstance(token, str)
        and isinstance(jwt["token_type"], str)
    )

    # Create task

    response = test_client.post(
        "/tasks/",
        json={"title": "create_task", "description": "test new task creation"},
        headers=auth_headers(token),
    )

    assert response.status_code == status.HTTP_201_CREATED

    create_task = response.json()
    task_id = create_task["id"]

    assert create_task["title"] == "create_task"
    assert create_task["description"] == "test new task creation"
    assert create_task["id"] == task_id
    assert isinstance(create_task["user_id"], int)
    assert create_task["completed"] is False
    assert isinstance(create_task["created_at"], str)

    # Verify task created through get task by id

    response = test_client.get(
        f"/tasks/{create_task['id']}", headers=auth_headers(token)
    )

    assert response.status_code == status.HTTP_200_OK

    get_task = response.json()

    assert get_task["title"] == "create_task"
    assert get_task["description"] == "test new task creation"
    assert get_task["id"] == task_id
    assert isinstance(get_task["user_id"], int)
    assert get_task["completed"] is False
    assert isinstance(get_task["created_at"], str)

    # Update task

    response = test_client.put(
        f"/tasks/{get_task['id']}",
        headers=auth_headers(token),
        json={
            "title": "updated_title",
            "description": "updated_description",
            "completed": True,
        },
    )

    assert response.status_code == status.HTTP_200_OK

    update_task = response.json()

    assert update_task["title"] == "updated_title"
    assert update_task["description"] == "updated_description"
    assert update_task["completed"] is True
    assert update_task["id"] == task_id
    assert isinstance(update_task["user_id"], int)
    assert isinstance(update_task["created_at"], str)

    # Delete task

    response = test_client.delete(
        f"/tasks/{update_task['id']}",
        headers=auth_headers(token),
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Verify task deleted

    response = test_client.get(
        f"/tasks/{create_task['id']}", headers=auth_headers(token)
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
