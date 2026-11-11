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

books = [
    Book(id=1, title="Atomic Habits", author="James Clear", pages=320, available=True),
    Book(id=2, title="The Alchemist", author="Paulo Coelho", pages=208, available=True),
    Book(id=3, title="Rich Dad Poor Dad", author="Robert Kiyosaki", pages=336, available=True),
    Book(id=4, title="Deep Work", author="Cal Newport", pages=304, available=True),
    Book(id=5, title="The Psychology of Money", author="Morgan Housel", pages=256, available=True),
    Book(id=6, title="Ikigai", author="Hector Garcia", pages=208, available=True),
    Book(id=7, title="Think and Grow Rich", author="Napoleon Hill", pages=320, available=False),
    Book(id=8, title="The Power of Habit", author="Charles Duhigg", pages=400, available=True),
    Book(id=9, title="Zero to One", author="Peter Thiel", pages=224, available=False),
    Book(id=10, title="The 7 Habits of Highly Effective People", author="Stephen Covey", pages=381, available=True),
] 
next_id = 11 

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

@app.get("/books/stats")
def stats(): 
    total = len(books)
    available = len(
        [b for b in books if b.available == True ]
    )
    borrowed = total - available 
    return {
        "total": total,
        "available": available,
        "borrowed": borrowed
    }