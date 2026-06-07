from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

class Task(BaseModel):
    id: int 
    title: str = None
    description: None = None
    completed: None = None
    create_at: None = None
    
# Temp list for the tasks    
tasks = ["ringo", "apple"]

app = FastAPI()

@app.get("/tasks")
def get_tasks():
    
    return tasks
    
@app.get("/tasks/{id}")
def get_task(id):
    None
    
@app.post("/tasks")
def create_task(task: Task):
    tasks.append(task)
    
    return task
    
@app.put("/tasks/{id}")
def put_task(id):
    None
    
@app.delete("/tasks/{id}")
def delete_task(id):
    None