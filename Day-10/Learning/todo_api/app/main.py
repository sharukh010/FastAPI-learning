from fastapi import FastAPI 
from app.routers import todos 
from app.exceptions import TodoNotFound, todo_not_found_handler, EmptyTitle, empty_title_handler


app = FastAPI(title="Todo API")
app.include_router(todos.router)
app.add_exception_handler(TodoNotFound,todo_not_found_handler)
app.add_exception_handler(EmptyTitle,empty_title_handler)

@app.get("/health")
def health(): 
    return {"status": "ok"}