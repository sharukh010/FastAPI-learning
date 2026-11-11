from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Book Library API")

class BookCreate(BaseModel): 
    title: str 
    author: str 
    pages: int 

class Book(BookCreate): 
    id: int 
    available: bool = True 

books = [] 
next_id = 1 

@app.get("/health")
def health(): 
    return {"status": "ok"}

@app.post("/books",status_code=201,response_model=Book)
def create_book(payload: BookCreate): 
    global next_id
    book = Book(id=next_id,**payload.model_dump())
    next_id += 1 
    books.append(book)
    return book 