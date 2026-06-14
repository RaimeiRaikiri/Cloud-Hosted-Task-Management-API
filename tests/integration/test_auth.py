from fastapi.testclient import TestClient
from app.auth import get_current_user
from fastapi import status

BASEURL = "/auth"

def test_access_token_authorized(test_client: TestClient, user):
    response = test_client.post(
        f"{BASEURL}/token",
        data="username=test&password=password",
        headers={
            "content-type":"application/x-www-form-urlencoded"
            }
        )
    
    json_response = response.json()
    
    assert isinstance(json_response["access_token"], str) \
           and isinstance(json_response["token_type"], str)
           
    assert response.status_code == status.HTTP_200_OK
    
def test_access_token_unauthorized(test_client: TestClient):
    response = test_client.post(
        f"{BASEURL}/token", 
        data="username=wrong&password=wrong",
        headers={
            "content-type":"application/x-www-form-urlencoded"
            }
        )
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    