from fastapi import FastAPI,status, Request, Query
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from errors import TodoNotFound
from datetime import datetime 
from zoneinfo import ZoneInfo
from schemas import TodoCreate, Todo , TodoPatch , Priority, SortBy,SortOrder, TodoListResponse
from datetime import datetime, date
from storage import next_id , todos 

zone = ZoneInfo("Asia/Kolkata")

app = FastAPI(title="Todo API")

@app.exception_handler(TodoNotFound)
async def not_found(request: Request, exc: TodoNotFound): 
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content = {
            "error": "not_found",
            "message": f"Todo {exc.id} not found"
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_error(request: Request,exc: RequestValidationError): 
    return JSONResponse(
        status_code = status.HTTP_422_UNPROCESSABLE_CONTENT,
        content = {
            "error": "validation_error",
            "message": exc.errors()
        }
    )

@app.exception_handler(Exception)
async def error_handler(request: Request,exc: Exception):
    print(exc) 
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "internal_server_error",
            "message": "something went wrong"
        }
    )

@app.get("/health")
def health(): 
    return {
        "status": "ok"
    }

@app.post("/todos",response_model=Todo,status_code=status.HTTP_201_CREATED)
def create_todo(payload: TodoCreate): 
    global next_id 

    current_time = datetime.now(zone)
    todo = Todo(id=next_id,**payload.model_dump(),created_at=current_time,updated_at=current_time)
    todos[next_id] = todo 
    next_id += 1 
    return todo 

@app.get("/todos",response_model=TodoListResponse,status_code=status.HTTP_200_OK)
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
    # TODO: add the logic of filtering 

    result = list(todos.values())
    result = result[offset:offset+limit]
    response = TodoListResponse(
        total=len(result),
        limit=limit,
        offset=offset,
        items=result,
    )
    return response 