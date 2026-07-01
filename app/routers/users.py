from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import app.database_models as database_models
from app.database import get_db
from app.models import User, UserCreate
from app.routers.auth import get_current_user, get_password_hash

router = APIRouter(prefix="/users", tags=["Users"])

db = Annotated[Session, Depends(get_db)]
current_user = Annotated[User, Depends(get_current_user)]


# Users
@router.post("/", status_code=status.HTTP_201_CREATED)
def register_user(new_user: UserCreate, db: db):

    existing_username = (
        db.query(database_models.User)
        .filter(database_models.User.username == new_user.username)
        .first()
    )

    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Username already exists"
        )

    existing_email = (
        db.query(database_models.User)
        .filter(database_models.User.email == new_user.email)
        .first()
    )

    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already in use for a different user",
        )

    hashed_password = get_password_hash(new_user.password)

    db_user = UserCreate(
        username=new_user.username, email=new_user.email, password=hashed_password
    )

    db.add(database_models.User(**db_user.model_dump()))
    db.commit()

    return {"username": new_user.username}


@router.get("/me")
async def root(current_user: current_user):
    return current_user
