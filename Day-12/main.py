from fastapi import FastAPI , Depends , HTTPException, status
from sqlalchemy.orm import Session 
import crud,models,schemas 
from database import engine,get_db


models.Base.metadata.create_all(bind=engine)
app = FastAPI()

@app.get("/health")
def health(): 
    return {"status": "ok"}

@app.post("/todos",response_model=schemas.TodoOut)
def create_todo(payload: schemas.TodoCreate, db: Session = Depends(get_db)): 
    payload.title = payload.title.strip()
    if payload.description is not None: 
        payload.description = payload.description.strip()
    todo = crud.create_todo(db,payload)
    return todo 

@app.get("/todos",response_model=list[schemas.TodoOut])
def list_todos(offset: int = 0 , limit: int = 10 ,done: bool | None = None , order_by: schemas.OrderBy = schemas.OrderBy.created_at ,db: Session = Depends(get_db)): 
    todos = crud.list_todos(db,offset,limit,done,order_by)
    return todos 

@app.get("/todos/{todo_id}",response_model=schemas.TodoOut)
def get_todo(todo_id: int, db: Session = Depends(get_db)): 
    todo = crud.get_todo(db,todo_id)
    if todo is None: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "not_found",
                "message": f"Todo with id {todo_id} not found"
            }
        )
    return todo 

@app.put("/todos/{todo_id}",response_model=schemas.TodoOut)
def replace_todo(todo_id: int , payload: schemas.TodoCreate,db: Session = Depends(get_db)): 
    payload.title = payload.title.strip()
    if payload.description is not None: 
        payload.description = payload.description.strip()
    
    todo = crud.get_todo(db,todo_id)
    if todo is None: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "not_found",
                "message": f"Todo with id {todo_id} not found"
            }
        )
    todo = crud.update_todo(db,todo,payload)
    return todo 

@app.patch("/todos/{todo_id}",response_model=schemas.TodoOut)
def update_todo(todo_id: int, payload: schemas.TodoUpdate, db: Session = Depends(get_db)): 
    if payload.title is not None: 
        payload.title = payload.title.strip()
    if payload.description is not None: 
        payload.description = payload.description.strip()

    todo = crud.get_todo(db,todo_id)
    if todo is None: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "not_found",
                "message": f"Todo with id {todo_id} not found"
            }
        )
    todo = crud.update_todo(db,todo,payload)
    return todo 

@app.delete("/todos/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
def delet_todo(todo_id: int,db: Session = Depends(get_db)): 
    todo = crud.get_todo(db,todo_id)
    if todo is None: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "not_found",
                "message": f"Todo with id {todo_id} not found"
            }
        )
    crud.delete_todo(db,todo)