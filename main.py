from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel
from datetime import datetime
from database import session, engine
import database_models
from sqlalchemy.orm import Session
from auth import router, get_password_hash, get_current_active_user
from database import get_db
from models import UserCreate, TaskCreate, TaskResponse, TaskUpdate, User

app = FastAPI()
app.include_router(router)

database_models.Base.metadata.create_all(bind=engine)
    
task_one = TaskCreate(
    title="test1",
    description="testing time",
)
task_two = TaskCreate(
    title="test2",
    description="testing time",
)

# Temp list for the tasks    
tasks = [task_one, task_two]
        
# Inital testing data into db
def init_db():
    db = session()
    
    count = db.query(database_models.Task).count()
    
    if count == 0:
        for task in tasks:
            db.add(database_models.Task(
                **task.model_dump(),
                completed = False
                ))
        
        db.commit()
        db.close()

init_db()

# Users
@app.post("/users", status_code=status.HTTP_201_CREATED)
def register_user(new_user: UserCreate, db: Session = Depends(get_db)):
    
    existing = db.query(database_models.User).filter(
        database_models.User.username == new_user.username).first()
    
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")
    
    print(new_user.password)
    hashed_password = get_password_hash(new_user.password)
    
    
    db_user = UserCreate(
        username=new_user.username,
        password=hashed_password
    )
    
    db.add(database_models.User(**db_user.model_dump()))
    db.commit()
    
    return {"username":new_user.username}

@app.get("/users/me")
async def root(current_user: User = Depends(get_current_active_user)):
    return current_user

# Tasks
@app.get("/tasks", response_model=list[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    
    number_of_tasks = db.query(database_models.Task).count()
    
    if number_of_tasks > 0:
        db_tasks = db.query(database_models.Task).all()
        
        return db_tasks
    else:
        return []
    
@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task_in_db = db.query(database_models.Task).filter(database_models.Task.id == task_id).first()
    
    if task_in_db:
        
        return task_in_db
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found"
        )
    
@app.post("/tasks", status_code=status.HTTP_201_CREATED, response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    db.add(database_models.Task(
        **task.model_dump(),
        completed = False
        ))
    db.commit()
    
    return task
    
@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    try:
        task_in_db = db.query(database_models.Task).filter(database_models.Task.id == task_id).first()
        if task_in_db:
            if task.title:
                task_in_db.title = task.title
            if task.description:
                task_in_db.description = task.description
            if task.completed:
                task_in_db.completed = task.completed
            
            db.commit()
            
            return task_in_db
            
    except:
        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found"
        )
    
@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    try:
        task_in_db = db.query(database_models.Task).filter(database_models.Task.id == task_id).first()
        if task_in_db:
            db.delete(task_in_db)
            db.commit()
            
            return None
    except:
        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found"
        )