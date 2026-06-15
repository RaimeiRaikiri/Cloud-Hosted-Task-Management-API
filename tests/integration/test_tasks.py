from fastapi.testclient import TestClient
from fastapi import status
from app.database_models import Task

def auth_headers(token):
    
    return {"Authorization":f"Bearer {token}"}

# Get all tasks from current user endpoints

def test_get_all_tasks(test_client: TestClient, task, token):
    
    response = test_client.get(
        "/tasks",
        headers=auth_headers(token))
    
    response_json = response.json()
    
    assert isinstance(response_json, list)
    
    assert isinstance(response_json[0], dict)
    assert response_json[0]["title"] == "test"
    
    assert response.status_code == status.HTTP_200_OK
    
def test_get_all_tasks_empty(test_client: TestClient, token, task):
    
    response = test_client.get(
        "/tasks",
        headers=auth_headers(token))
    
    response_json = response.json()
    
    assert isinstance(response_json, list)
    assert response.status_code == status.HTTP_200_OK
    
def test_get_all_tasks_unauthenticated(test_client: TestClient, task):
    
    response = test_client.get("/tasks")
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    
# Get task by id endpoints

def test_get_task_by_id(test_client: TestClient, token, task):
    
    response = test_client.get(
        f"/tasks/{task.id}",
        headers=auth_headers(token)
        )
    response_json = response.json()

    assert isinstance(response_json, dict)
    assert response.status_code == status.HTTP_200_OK

def test_get_task_by_id_unauthenticated(test_client: TestClient, task):
    
    response = test_client.get(f"tasks/{task.id}")
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
def test_get_task_by_id_not_found(test_client: TestClient, token):
    
    response = test_client.get(
        "tasks/99999",
        headers=auth_headers(token)
        )
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    
def test_get_task_by_id_forbidden(
    test_client: TestClient,
    token, 
    second_user_task,
    second_user):
    
    response = test_client.get(
        f"tasks/{second_user_task.id}",
        headers=auth_headers(token)
        )
    
    assert response.status_code == status.HTTP_403_FORBIDDEN
    