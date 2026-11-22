from fastapi import FastAPI, Depends 
from sqlalchemy.orm import Session 
from sqlalchemy import select 


from database import engine,Base,get_db 
import models,schemas 

#creates tables if they don't exist 
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/todos",response_model=schemas.TodoOut,status_code=201)
def create_todo(data: schemas.TodoCreate,db: Session = Depends(get_db)): 
    todo = models.Todo(**data.model_dump())
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo 

@app.get("/todos",response_model=list[schemas.TodoOut])
def list_todos(db: Session = Depends(get_db)): 
    return db.scalars(select(models.Todo)).all()