from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(title = "Karishma's to do API")

@app.get("/")
def read_root():
    return {"message": "Welcome to Karishma's To-Do API"}

class TodoItem(BaseModel):
    id: int
    task: str
    completed: bool = False

db: List[TodoItem] = []

@app.post("/todos/", response_model=TodoItem)
def create_todo(todo: TodoItem):
    db.append(todo)
    return todo

@app.get("/todos/", response_model=List[TodoItem])
def read_todos(): 
    return db

@app.put("/todos/{todo_id}", response_model=TodoItem)
def update_todo(todo_id: int, updated_task: TodoItem):
    for index, todo in enumerate(db):
        if todo.id == todo_id:
            db[index] = updated_task
            return updated_task
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    for index, todo in enumerate(db):
        if todo.id == todo_id:
            del db[index]
            return {"message": "Task {todo_id} deleted successfully"}
    raise HTTPException(status_code=404, detail="Task not found")
