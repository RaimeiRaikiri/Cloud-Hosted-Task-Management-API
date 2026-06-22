from fastapi import FastAPI

import app.database_models as database_models
import app.routers.auth as auth
import app.routers.tasks as tasks
import app.routers.users as users
from app.database import engine

app = FastAPI(
    title="Task Manager API",
    description="Task Management API with JWT authentication",
    version="1.0.0",
)

app.include_router(auth.router)
app.include_router(tasks.router)
app.include_router(users.router)


@app.on_event("startup")
def startup():
    database_models.Base.metadata.create_all(bind=engine)
