from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
import app.exceptions as exceptions 
from app.routers import todos 
from app.models import Base 
from app.database import engine 

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Todo API")
app.include_router(todos.router)


# adding exception handlers 
app.add_exception_handler(exceptions.TodoNotFound,exceptions.not_found)
app.add_exception_handler(exceptions.DuplicateTitle,exceptions.duplicate_title)
app.add_exception_handler(exceptions.EmptyTitle,exceptions.empty_title)
app.add_exception_handler(RequestValidationError,exceptions.validation_error)
app.add_exception_handler(Exception,exceptions.error_handler)


@app.get("/health")
def health(): 
    return {
        "status": "ok"
    }