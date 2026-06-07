from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from datetime import datetime

class Task(BaseModel):
    id: int = None
    title: str = None
    description: str = None
    completed: bool = None
    create_at: None = None
    
task_one = Task(
    id=5,
    title="test1",
    description="testing time",
    completed=False,
    create_at=None
)
task_two = Task(
    id=3,
    title="test2",
    description="testing time",
    completed=False,
    create_at=None
)

# Temp list for the tasks    
tasks = [task_one, task_two]

app = FastAPI()

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