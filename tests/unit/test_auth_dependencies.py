from app.models import Token
from app.auth import get_password_hash, verify_password, create_access_token
from datetime import timedelta
import os 
from dotenv import load_dotenv
import jwt

load_dotenv()

ALGORITHM = "HS256"
SECRET_KEY = os.getenv("SECRET_KEY")
BASEURL = "/auth"

def test_verify_password():
    hashed_password = get_password_hash("password")
    
    assert verify_password("password", hashed_password)
    assert not verify_password("not password", hashed_password)
    
def test_password_hash():
    
    assert isinstance(get_password_hash("password"), str)

def test_create_access_token():
    access_token_expires = timedelta(minutes=15)
    data={"sub": "john"}
    access_token = create_access_token(
        data=data,
        expires_delta=access_token_expires
    )
    
    assert isinstance(access_token, str)
    
    payload = jwt.decode(
        access_token, 
        SECRET_KEY, 
        algorithms=[ALGORITHM])
    
    
    assert payload["sub"] == "john"
    assert "exp" in payload
     

