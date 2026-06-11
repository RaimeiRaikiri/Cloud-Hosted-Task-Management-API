from pydantic import BaseModel

# For main.py
class TaskCreate(BaseModel):
    title: str
    description: str

class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    completed: bool | None = None
    
class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    completed: bool
    created_at: str | None = None
    
    user_id: int | None = None

class UserCreate(BaseModel):
    username: str
    email: str
    password: str


# For Auth
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    username: str | None = None

class User(BaseModel):
    username: str
    disabled: bool | None = None
    
class UserInDb(User):
    id: int
    password: str