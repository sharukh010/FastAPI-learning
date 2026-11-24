from sqlalchemy import select 
from sqlalchemy.orm import Session 
import models, schemas 

def create_todo(db: Session, data: schemas.TodoCreate): 
    todo = models.Todo(**data.model_dump())
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo 

def get_todo(db: Session, todo_id: int): 
    return db.get(models.Todo,todo_id)

def list_todos(db: Session,skip = 0 , limit = 10 , done: bool | None = None,order_by: str | None = None): 
    stmt = select(models.Todo)
    if done is not None: 
        stmt = stmt.where(models.Todo.done == done)
    return db.scalars(stmt.offset(skip).limit(limit).order_by(order_by)).all()

def update_todo(db: Session, todo: models.Todo, data: schemas.TodoUpdate): 
    for k,v in data.model_dump(exclude_unset=True).items(): 
        setattr(todo,k,v)
    db.commit()
    db.refresh()
    return todo 

def delete_todo(db: Session, todo: models.Todo): 
    db.delete(todo)
    db.commit()