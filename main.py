from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel
from datetime import datetime
from database import session, engine
import database_models
from sqlalchemy.orm import Session

app = FastAPI()

database_models.Base.metadata.create_all(bind=engine)

class TaskCreate(BaseModel):
    title: str
    description: str

class TaskUpdate(BaseModel):
    title: str
    description: str
    completed: bool
    
class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    completed: bool
    created_at: str|None = None
    
    user_id: int|None = None

class UserCreate(BaseModel):
    username: str
    password: str
    
task_one = Task(
    id=5,
    title="test1",
    description="testing time",
    completed=False,
    created_at=""
)
task_two = Task(
    id=3,
    title="test2",
    description="testing time",
    completed=False,
    created_at=""
)

# Temp list for the tasks    
tasks = [task_one, task_two]

def get_db():
    db = session()
    try:
        yield db
    # Close the connection to db regardless of yield outcome 
    finally:
        db.close()
        
# Inital testing data into db
def init_db():
    db = session()
    
    count = db.query(database_models.Task).count()
    
    if count == 0:
        for task in tasks:
            db.add(database_models.Task(**task.model_dump()))
        
        db.commit()
        db.close()

init_db()

@app.get("/tasks", response_model=list[Task])
def get_tasks(db: Session = Depends(get_db)):
    
    number_of_tasks = db.query(database_models.Task).count()
    
    if number_of_tasks > 0:
        db_tasks = db.query(database_models.Task).all()
        
        return db_tasks
    else:
        return []
    
@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task_in_db = db.query(database_models.Task).filter(database_models.Task.id == task_id).first()
    
    if task_in_db:
        
        return task_in_db
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found"
        )
    
@app.post("/tasks", status_code=status.HTTP_201_CREATED, response_model=Task)
def create_task(task: Task, db: Session = Depends(get_db)):
    db.add(database_models.Task(**task.model_dump()))
    db.commit()
    
    return task
    
@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task: Task, db: Session = Depends(get_db)):
    try:
        task_in_db = db.query(database_models.Task).filter(database_models.Task.id == task_id).first()
        if task_in_db:
            
            task_in_db.title = task.title
            task_in_db.description = task.description
            task_in_db.completed = task.completed
            task_in_db.created_at = task.created_at
            
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