from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi import Request,status 
from main import app 

class TodoNotFound(Exception): 
    def __init__(self,todo_id): 
        self.id = todo_id 

@app.exception_handlers(TodoNotFound)
async def not_found(request: Request, exc: TodoNotFound): 
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content = {
            "error": "not_found",
            "message": f"Todo {exc.id} not found"
        }
    )

@app.exception_handlers(RequestValidationError)
async def validation_error(request: Request,exc: RequestValidationError): 
    return JSONResponse(
        status_code = status.HTTP_422_UNPROCESSABLE_CONTENT,
        content = {
            "error": "validation_error",
            "message": exc.errors()
        }
    )

@app.exception_handlers(Exception)
async def error_handler(request: Request,exc: Exception):
    print(exc) 
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "internal_server_error",
            "message": "something went wrong"
        }
    )