from fastapi import FastAPI, HTTPException,Query
from pydantic import BaseModel
from typing import Annotated

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

@app.get("/books")
def list_books(
    author: Annotated[str | None ,Query(min_length=2)]=None,
    available: bool = False,
    search: Annotated[str | None ,Query(min_length=4)]=None,
    skip: Annotated[int,Query(ge=0)]=0,
    limit: Annotated[int,Query(ge=0)]=10
): 
    result = None 
    if author is None: 
        result = books 
    else: 
        result = [b for b in books if b.author.lower() == author.lower()]

    if available is True: 
        result = [b for b in result if b.available == True]

    if search is not None: 
        result = [b for b in result if b.title.lower() == search.lower()]

    result = result[skip:skip+limit]
    return result