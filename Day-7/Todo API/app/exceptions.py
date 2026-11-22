from fastapi.responses import JSONResponse
from fastapi import status, Request
from fastapi.exceptions import RequestValidationError

class TodoNotFound(Exception): 
    def __init__(self,todo_id): 
        self.id = todo_id 

async def not_found(request: Request, exc: TodoNotFound): 
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content = {
            "error": "not_found",
            "message": f"Todo with id {exc.id} not found"
        }
    )

class DuplicateTitle(Exception): 
    def __init__(self,title): 
        self.title = title 

async def duplicate_title(request: Request, exc: DuplicateTitle): 
    return JSONResponse(
        status_code = status.HTTP_409_CONFLICT,
        content= {

            "error": "duplicate_title",
            "message": f"todo with title '{exc.title}' already exists" 
        }
    )

class EmptyTitle(Exception): 
    pass 

async def empty_title(request: Request, exc: EmptyTitle): 
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={
            "error": "empty_title",
            "message": "title cannot be empty"
        }
    )

async def validation_error(request: Request,exc: RequestValidationError): 
    return JSONResponse(
        status_code = status.HTTP_422_UNPROCESSABLE_CONTENT,
        content = {
            "error": "validation_error",
            "message": exc.errors()
        }
    )

async def error_handler(request: Request,exc: Exception):
    print(exc) 
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "internal_server_error",
            "message": "something went wrong"
        }
    )