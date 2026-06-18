from fastapi import status
from fastapi.testclient import TestClient

from app.database_models import Task


def auth_headers(token):

    return {"Authorization": f"Bearer {token}"}


# Get all tasks from current user endpoints


def test_get_all_tasks(test_client: TestClient, task, token):

    response = test_client.get("/tasks", headers=auth_headers(token))

    response_json = response.json()

    assert isinstance(response_json, list)

    assert isinstance(response_json[0], dict)
    assert response_json[0]["title"] == "test"

    assert response.status_code == status.HTTP_200_OK


def test_get_all_tasks_empty(test_client: TestClient, token, task):

    response = test_client.get("/tasks", headers=auth_headers(token))

    response_json = response.json()

    assert isinstance(response_json, list)
    assert response.status_code == status.HTTP_200_OK


def test_get_all_tasks_unauthenticated(test_client: TestClient, task):

    response = test_client.get("/tasks")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


# Get task by id endpoints


def test_get_task_by_id(test_client: TestClient, token, task):

    response = test_client.get(f"/tasks/{task.id}", headers=auth_headers(token))
    response_json = response.json()

    assert isinstance(response_json, dict)
    assert response.status_code == status.HTTP_200_OK


def test_get_task_by_id_unauthenticated(test_client: TestClient, task):

    response = test_client.get(f"tasks/{task.id}")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_task_by_id_not_found(test_client: TestClient, token):

    response = test_client.get("tasks/99999", headers=auth_headers(token))

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_task_by_id_forbidden(
    test_client: TestClient, token, second_user_task, second_user
):

    response = test_client.get(
        f"tasks/{second_user_task.id}", headers=auth_headers(token)
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


# Post/Create task endpoint


def test_create_task(test_client: TestClient, token, db):

    response = test_client.post(
        "/tasks",
        json={"title": "create_task", "description": "test new task creation"},
        headers=auth_headers(token),
    )

    response_json = response.json()
    assert response.status_code == status.HTTP_201_CREATED
    assert isinstance(response_json, dict)

    new_task = db.query(Task).filter(Task.id == response_json["id"]).first()

    assert new_task is not None
    assert new_task.description == "test new task creation"


def test_create_task_unauthenticated(test_client: TestClient):

    response = test_client.post(
        "/tasks", json={"title": "create_task", "description": "test new task creation"}
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


# Put/Update task by id endpoints


def test_update_task_by_id(test_client: TestClient, token, task, db):

    response = test_client.put(
        f"/tasks/{task.id}",
        json={
            "title": "updated_title",
            "description": "updated_description",
            "completed": True,
        },
        headers=auth_headers(token),
    )

    response_json = response.json()

    assert isinstance(response_json, dict)
    assert response.status_code == status.HTTP_200_OK

    # Ensure db updates
    db.expire_all()
    updated_task = db.query(Task).filter(Task.id == task.id).first()

    assert updated_task is not None
    assert (
        updated_task.title == "updated_title"
        and updated_task.description == "updated_description"
        and updated_task.completed
    )


def test_update_task_by_id_unauthenticated(test_client: TestClient, task):

    response = test_client.put(
        f"/tasks/{task.id}",
        json={
            "title": "updated_title",
            "description": "updated_description",
            "completed": True,
        },
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_update_task_by_id_not_found(test_client: TestClient, token):

    response = test_client.put(
        "/tasks/99999",
        json={
            "title": "updated_title",
            "description": "updated_description",
            "completed": True,
        },
        headers=auth_headers(token),
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_task_by_id_forbidden(
    test_client: TestClient, token, second_user_task, second_user
):

    response = test_client.put(
        f"/tasks/{second_user_task.id}",
        json={
            "title": "updated_title",
            "description": "updated_description",
            "completed": True,
        },
        headers=auth_headers(token),
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


# Delete task by id


def test_delete_task_by_id(test_client: TestClient, token, task, db):

    response = test_client.delete(f"/tasks/{task.id}", headers=auth_headers(token))
    task_id = task.id

    assert response.status_code == status.HTTP_204_NO_CONTENT

    db.expire_all()
    deleted_task = db.query(Task).filter(Task.id == task_id).first()

    assert deleted_task is None


def test_delete_task_by_id_unauthenticated(test_client: TestClient, task):

    response = test_client.delete(f"/tasks/{task.id}")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_delete_task_by_id_not_found(test_client: TestClient, token):

    response = test_client.delete("/tasks/99999", headers=auth_headers(token))

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_task_by_id_forbidden(
    test_client: TestClient, token, second_user, second_user_task
):

    response = test_client.delete(
        f"/tasks/{second_user_task.id}", headers=auth_headers(token)
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
