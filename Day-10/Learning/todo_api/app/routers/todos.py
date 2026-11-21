from fastapi import APIRouter, HTTPException, Depends , status
from app.schemas import TodoCreate, Todo, zone 
from app.dependencies import pagination 
from app import storage 
from datetime import datetime 
from uuid import uuid4, UUID
from app.exceptions import TodoNotFound, EmptyTitle

router = APIRouter(
    prefix="/todos",
    tags=["Todos"],
    responses={404: {"description": "Not found"}},
)

@router.get("/",response_model=list[Todo])
def list_todos(page: dict = Depends(pagination)): 
    todos = list(storage.todos.values())
    return todos[page["skip"]: page["skip"]+page["limit"]]

@router.post("/",response_model=Todo)
def create_todo(payload: TodoCreate): 
    payload.title = payload.title.strip()
    if len(payload.title) == 0: 
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail={"description": "Title cannot be empty"}
        )
    if payload.description is not None: 
        payload.description = payload.description.strip()

    created_at = datetime.now(zone)
    updated_at = datetime.now(zone)
    todo_id = uuid4()

    storage.todos[todo_id] = Todo(**payload.model_dump(),id=todo_id,created_at=created_at,updated_at=updated_at)
    return storage.todos[todo_id]

@router.get("/{todo_id}")
def get_todo(todo_id: UUID): 
    if todo_id not in storage.todos: 
        raise TodoNotFound(todo_id)
    return storage.todos[todo_id]