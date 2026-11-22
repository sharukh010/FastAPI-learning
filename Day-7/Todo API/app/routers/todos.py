from fastapi import APIRouter , status, Query, Path 
from app.schemas import TodoCreate, Todo , TodoPatch , Priority, SortBy,SortOrder, TodoListResponse, StatsResponse
from datetime import datetime, date, timedelta 
from app.storage import next_id, todos,isTitleUnique, process_and_check_title 
from zoneinfo import ZoneInfo
import app.exceptions as exceptions 
from typing import Annotated

zone = ZoneInfo("Asia/Kolkata")

router = APIRouter(
    prefix="/todos",
    tags = ["Todos"],
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "not found"
        }
    }
)

@router.post("/",response_model=Todo,status_code=status.HTTP_201_CREATED)
def create_todo(payload: TodoCreate): 
    global next_id 

    current_time = datetime.now(zone)
    payload.title = process_and_check_title(payload.title)
    payload.description = payload.description.strip()
    todo = Todo(id=next_id,**payload.model_dump(),created_at=current_time,updated_at=current_time)
    todos[next_id] = todo 
    next_id += 1 
    return todo 

@router.get("/",response_model=TodoListResponse,status_code=status.HTTP_200_OK)
def list_todos(
    completed: bool | None  = None ,
    priority: Priority | None = None , 
    search: str | None = Query(default=None,min_length=1),
    due_before: date | None = None, 
    due_after: date | None = None ,
    sort_by: SortBy = SortBy.created_at,
    order: SortOrder = SortOrder.asc , 
    limit: int = Query(default=10,ge=1,le=100),
    offset: int = Query(default=0,ge=0)
): 
    priority_values = {Priority.low: 1, Priority.medium: 2,Priority.high: 3}

    result = list(todos.values())
    if search is not None: 
        result = [t for t in result if search.lower() in t.title.lower()]
    if completed is not None: 
        result = [t for t in result if t.completed == completed]
    if due_before is not None: 
        result = [t for t in result if t.due_date is not None and (due_before-t.due_date).days>0]
    if due_after is not None: 
        result = [t for t in result if t.due_date is not None and (t.due_date-due_after).days >0]
    if priority is not None: 
        result = [t for t in result if t.priority == priority]


    total = len(result)
    result = result[offset:offset+limit]
    if sort_by == SortBy.due_date: 
        result.sort(key=lambda x: x.due_date if x.due_date is not None else (datetime.now(zone).date()+timedelta(100)))
    elif sort_by == SortBy.title: 
        result.sort(key=lambda x: x.title.lower())
    elif sort_by == SortBy.created_at: 
        result.sort(key=lambda x: x.created_at)
    elif sort_by == SortBy.priority: 
        result.sort(key=lambda x: priority_values[x.priority])
    
    print(result)

    if order == SortOrder.desc: 
        result = result[::-1]

    response = TodoListResponse(
        total=total,
        limit=limit,
        offset=offset,
        items=result,
    )
    return response 

@router.get("/stats",response_model=StatsResponse,status_code=status.HTTP_200_OK)
def get_stats(): 
    today = datetime.now(zone).date()
    total = len(todos.values())
    completed = len([t for t in todos.values() if t.completed == True])
    pending = len([t for t in todos.values() if t.completed == False])
    low = len([t for t in todos.values() if t.priority == Priority.low])
    medium = len([t for t in todos.values() if t.priority == Priority.medium])
    high = len([t for t in todos.values() if t.priority == Priority.high])
    over_due = len([t for t in todos.values() if t.due_date is not None and (t.due_date-today).days < 0 ])
    response = StatsResponse(
        total=total,
        completed=completed,
        pending=pending,
        overdue=over_due,
        by_priority={"low": low,"medium": medium,"high": high}
    )
    return response 

@router.get("/{todo_id}",response_model=Todo,status_code=status.HTTP_200_OK)
def get_todo(todo_id:int = Path(ge=1)): 
    if todo_id not in todos: 
        raise exceptions.TodoNotFound(todo_id=todo_id)
    return todos[todo_id]

@router.put("/{todo_id}",response_model=Todo)
def replace_todo(todo_id:Annotated[int,Path(ge=1)],payload: TodoCreate): 
    if todo_id not in todos: 
        raise exceptions.TodoNotFound(todo_id=todo_id)
    old_todo = todos[todo_id]
    payload.title = payload.title = process_and_check_title(payload.title)
    payload.description = payload.description.strip()
    todos[todo_id] = Todo(id=old_todo.id,created_at=old_todo.created_at,**payload.model_dump(exclude_unset=True),updated_at=datetime.now(zone))
    return todos[todo_id]

@router.patch("/{todo_id}",response_model=Todo)
def update_todo(todo_id:Annotated[int,Path(ge=1)],payload: TodoPatch): 
    if todo_id not in todos: 
        raise exceptions.TodoNotFound
    if payload.title is not None: 
        payload.title = payload.title = process_and_check_title(payload.title)
    if payload.description is not None: 
        payload.description = payload.description.strip()
    old_todo = todos[todo_id]
    updated_todo = old_todo.model_dump()
    updated_todo.update(**payload.model_dump(exclude_unset=True),updated_at=datetime.now(zone))
    todos[todo_id] = updated_todo
    return todos[todo_id]

@router.delete("/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int = Path(ge=1)): 
    if todo_id not in todos: 
        raise exceptions.TodoNotFound(todo_id=todo_id)
    del todos[todo_id]

@router.delete("/")
def delete_completed_todos(completed: bool): 
    completed_todo_ids = [t.id for t in todos.values() if t.completed == completed]
    count = len(completed_todo_ids)
    for id in completed_todo_ids: 
        del todos[id]
    return {"deleted":count}