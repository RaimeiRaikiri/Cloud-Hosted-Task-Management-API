from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel
from datetime import datetime
from database import session, engine
import database_models
from sqlalchemy.orm import Session

app = FastAPI()

database_models.Base.metadata.create_all(bind=engine)

class Task(BaseModel):
    id: int = None
    title: str = None
    description: str = None
    completed: bool = None
    create_at: str = None
    
task_one = Task(
    id=5,
    title="test1",
    description="testing time",
    completed=False,
    create_at=""
)
task_two = Task(
    id=3,
    title="test2",
    description="testing time",
    completed=False,
    create_at=""
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
def get_tasks():
    if len(tasks) > 0:
        
        return tasks
    else:
        raise HTTPException(
            status_code=404, 
            detail="There are no tasks found"
        )
    
@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    if tasks[task_id]:
        
        return tasks[task_id]
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found"
        )
    
@app.post("/tasks", status_code=status.HTTP_201_CREATED, response_model=Task)
def create_task(task: Task):
    tasks.append(task)
    return task
    
@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task: Task):
    try:
        if tasks[task_id]:
            tasks[task_id] = task
            
            return task
            
    except:
        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found"
        )
    
@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    try:
        if tasks[task_id]:
            tasks[task_id] = None
            
            return None
    except:
        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found"
        )