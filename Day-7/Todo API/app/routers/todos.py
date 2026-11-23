from fastapi import APIRouter , status, Query, Path , Depends
from app.schemas import TodoCreate, Todo , TodoPatch , Priority, SortBy,SortOrder, TodoListResponse, StatsResponse
from app.dependencies import FilteringAndPaginationDep
from datetime import datetime, date, timedelta 
from app.storage import next_id, todos
from app.models import isTitleUnique, process_and_check_title 
from zoneinfo import ZoneInfo
import app.exceptions as exceptions 
import app.models as models   
from typing import Annotated
from sqlalchemy import select , delete , func , update 
from sqlalchemy.orm import Session 
from app.database import get_db

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
def create_todo(payload: TodoCreate,db: Session = Depends(get_db)): 
    payload.title = process_and_check_title(payload.title,db,todo_id)
    todo = models.Todo(**payload.model_dump())
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo 

@router.get("/",response_model=TodoListResponse,status_code=status.HTTP_200_OK)
def list_todos(
    p: Annotated[FilteringAndPaginationDep,Depends()],
    db: Session = Depends(get_db)
): 
    priority_values = {Priority.low: 1, Priority.medium: 2,Priority.high: 3}

    result = list(todos.values())
    if p.search is not None: 
        result = [t for t in result if p.search.lower() in t.title.lower()]
    if p.completed is not None: 
        result = [t for t in result if t.completed == p.completed]
    if p.due_before is not None: 
        result = [t for t in result if t.due_date is not None and (p.due_before-t.due_date).days>0]
    if p.due_after is not None: 
        result = [t for t in result if t.due_date is not None and (t.due_date-p.due_after).days >0]
    if p.priority is not None: 
        result = [t for t in result if t.priority == p.priority]


    total = len(result)
    result = result[p.offset:p.offset+p.limit]
    if p.sort_by == SortBy.due_date: 
        result.sort(key=lambda x: x.due_date if x.due_date is not None else (datetime.now(zone).date()+timedelta(100)))
    elif p.sort_by == SortBy.title: 
        result.sort(key=lambda x: x.title.lower())
    elif p.sort_by == SortBy.created_at: 
        result.sort(key=lambda x: x.created_at)
    elif p.sort_by == SortBy.priority: 
        result.sort(key=lambda x: priority_values[x.priority])
    
    print(result)

    if p.order == SortOrder.desc: 
        result = result[::-1]

    response = TodoListResponse(
        total=total,
        limit=p.limit,
        offset=p.offset,
        items=result,
    )
    return response 

@router.get("/stats",response_model=StatsResponse,status_code=status.HTTP_200_OK)
def get_stats(db: Session = Depends(get_db)): 
    today = datetime.now(zone).date()
    total = db.scalar(select(func.count()).select_from(models.Todo))
    completed = db.scalar(select(func.count()).select_from(models.Todo).where(
        models.Todo.completed == True
    ))
    pending = db.scalar(select(func.count()).select_from(models.Todo).where(
        models.Todo.completed == False
    ))
    low = db.scalar(select(func.count()).select_from(models.Todo).where(
        models.Todo.priority == Priority.low 
    ))
    medium = db.scalar(select(func.count()).select_from(models.Todo).where(
        models.Todo.priority == Priority.medium 
    ))
    high = db.scalar(select(func.count()).select_from(models.Todo).where(
        models.Todo.priority == Priority.high 
    ))
    over_due = db.scalar(
        select(func.count()).select_from(models.Todo).where(
            models.Todo.due_date != None,
            models.Todo.due_date  < today
        )
    ) 
    response = StatsResponse(
        total=total,
        completed=completed,
        pending=pending,
        overdue=over_due,
        by_priority={"low": low,"medium": medium,"high": high}
    )
    return response 

@router.get("/{todo_id}",response_model=Todo,status_code=status.HTTP_200_OK)
def get_todo(todo_id:int = Path(ge=1),db: Session = Depends(get_db)): 
    todo = db.get(models.Todo,todo_id)
    if todo is None: 
        raise exceptions.TodoNotFound(todo_id)
    return todo 

@router.put("/{todo_id}",response_model=Todo)
def replace_todo(todo_id:Annotated[int,Path(ge=1)],payload: TodoCreate,db: Session = Depends(get_db)): 
    payload.title  = process_and_check_title(payload.title,db,todo_id)
    payload.description = payload.description.strip()
    todo = db.scalar(
        update(models.Todo).where(
            models.Todo.id == todo_id
        ).values(**payload.model_dump()).returning(
            models.Todo
        )
    )
    db.commit()
    if todo is None: 
        raise exceptions.TodoNotFound(todo_id)

    return todo 

@router.patch("/{todo_id}",response_model=Todo)
def update_todo(todo_id:Annotated[int,Path(ge=1)],payload: TodoPatch,db:Session = Depends(get_db)): 
    if payload.title is not None: 
        payload.title = payload.title = process_and_check_title(payload.title,db,todo_id)
    if payload.description is not None: 
        payload.description = payload.description.strip()
    todo = db.scalar(
        update(models.Todo).where(
            models.Todo.id == todo_id
        ).values(**payload.model_dump(exclude_unset=True)).returning(
            models.Todo
        )
    )
    db.commit()
    if todo is None: 
        raise exceptions.TodoNotFound(todo_id)
    return todo 

@router.delete("/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int = Path(ge=1),db: Session = Depends(get_db)): 
    result = db.execute(
        delete(models.Todo).where(
            models.Todo.id == todo_id
        )
    )
    db.commit()
    if result.rowcount == 0: 
        raise exceptions.TodoNotFound(todo_id)
    return 

@router.delete("/")
def delete_completed_todos(completed: bool = True,db: Session = Depends(get_db)): 
    result = db.execute(
            delete(models.Todo).where(
                models.Todo.completed == completed
            )
        )
    db.commit()
    return {"deleted":result.rowcount}