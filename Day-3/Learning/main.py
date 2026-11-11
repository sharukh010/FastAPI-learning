from fastapi import FastAPI 
from pydantic import BaseModel 


app = FastAPI(title="Todo API")



class TodoCreate(BaseModel): 
    title: str 
    description: str | None = None 
    done: bool = False 
    priority: int = 1 

class Todo(TodoCreate): 
    id: int

todos = [] 
next_id = 1 

@app.post("/todos",response_model=Todo,status_code=201)
def create_todo(payload: TodoCreate): 
    global next_id 
    todo = Todo(id=next_id,**payload.model_dump())
    next_id += 1 
    todos.append(todo)
    return todo

@app.get("/todos",response_model=list[Todo])
def list_todos(done: bool | None = None): 
    if done is None: 
        return todos 
    return [t for t in todos if t.done == done]

@app.get("/todos/{todo_id}",response_model=Todo)
def get_todo(todo_id: int): 
    for t in todos: 
        if t.id == todo_id: 
            return t 
    return {"error": "not found"}

