from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
import app.exceptions as exceptions 
from app.routers import todos 


app = FastAPI(title="Todo API")
app.include_router(todos.route)


# adding exception handlers 
@app.add_exception_handler(exceptions.TodoNotFound,exceptions.not_found)
@app.add_exception_handler(exceptions.DuplicateTitle,exceptions.duplicate_title)
@app.exception_handler(exceptions.EmptyTitle,exceptions.empty_title)
@app.exception_handler(RequestValidationError,exceptions.validation_error)
@app.exception_handler(Exception,exceptions.error_handler)


@app.get("/health")
def health(): 
    return {
        "status": "ok"
    }