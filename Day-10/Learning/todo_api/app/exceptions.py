from fastapi import Request , status
from fastapi.responses import JSONResponse


class TodoNotFound(Exception): 
    def __init__(self,todo_id): 
        self.id = todo_id 

async def todo_not_found_handler(request: Request, exc: TodoNotFound): 
    return JSONResponse(
        status_code=404,
        content= {
            "error": "todo_not_found",
            "detail": f"Todo with id  {exc.id} not found"
        }
    )

class EmptyTitle(Exception): 
    pass 

async def empty_title_handler(request: Request,exc: EmptyTitle): 
    return JSONResponse(
        status_code= status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={
            "error": "empty_title",
            "detail": "Todo title cannot be empty"
        }
    )