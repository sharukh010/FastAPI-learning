from fastapi import FastAPI,HTTPException,Request,status 
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field 

app = FastAPI(title="Library API")

class BookIn(BaseModel): 
    isbn: str = Field(min_length=10,max_length=13,examples=["9789356991460"])
    title: str = Field(min_length=1,examples=["Let's Talk Mutual Funds: A Systematic, Smart Way to Make Them Work for You"])
    author: str = Field(min_length=3,examples=["Monika Halan"])
    year: int = Field(gt=0,le=2026,examples=[2023])

class BookUpdate(BaseModel): 
    isbn: str | None = Field(default=None,min_length=10,max_length=13,examples=["9789356991460"])
    title: str | None = Field(default=None,min_length=1,examples=["Let's Talk Mutual Funds: A Systematic, Smart Way to Make Them Work for You"])
    author: str | None = Field(default=None,min_length=3,examples=["Monika Halan"])
    year: int | None = Field(default=None,gt=0,le=2026,examples=[2023])

class Book(BookIn): 
    id: int 

books: dict[int,Book] = {}
next_id = 1 

class BookNotFound(Exception): 
    def __init__(self,book_id: int): 
        self.book_id = book_id 

@app.exception_handler(BookNotFound)
async def not_found_handler(request: Request, exc: BookNotFound): 
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content = {
            "error": "not_found",
            "message": f"Book {exc.book_id} not found"
        }
    )

class DuplicateISBN(Exception): 
    def __init__(self,isbn: str): 
        self.isbn = isbn 

@app.exception_handler(DuplicateISBN)
async def duplicate_handler(request: Request, exc: DuplicateISBN): 
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "error":"duplicate_isbn",
            "message": f"ISBN {exc.isbn} already exists"
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_handler(request: Request,exc: RequestValidationError): 
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content = {
            "error": "validation_error",
            "details": exc.errors()
        }
    )

@app.exception_handler(Exception)
async def exception_handler(request: Request,exc: Exception): 
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content = {
            "error": "internal_server_error",
            "details": "something went wrong"
        }
    )

@app.post("/books",response_model=Book,status_code=status.HTTP_201_CREATED)
def create_book(data: BookIn): 
    global next_id
    if any(b.isbn == data.isbn for b in books.values()): 
        raise DuplicateISBN(data.isbn)
    book = Book(id=next_id,**data.model_dump())
    books[next_id] = book 
    next_id += 1 
    return book 

@app.get("/books",response_model=list[Book],status_code=status.HTTP_200_OK)
def list_books(): 
    return list(books.values())

@app.get("/books/{book_id}",response_model=Book)
def get_book(book_id: int):
    if book_id not in books: 
        raise BookNotFound(book_id)
    return books[book_id]

@app.put("/books/{book_id}",response_model=Book)
def update_book(book_id: int, payload: BookIn): 
    if book_id not in books: 
        raise BookNotFound(book_id)
    if any(b.isbn == payload.isbn and b.id != book_id for b in books.values()): 
        raise DuplicateISBN(payload.isbn)
    books[book_id] = Book(id=book_id,**payload.model_dump())
    return books[book_id]

@app.patch("/books/{book_id}",response_model=Book)
def update_book_details(book_id:int, payload: BookUpdate): 
    if book_id not in books: 
        raise BookNotFound(book_id)
    if any (b.isbn == payload.isbn and b.id != book_id for b in books.values()): 
        raise DuplicateISBN(payload.isbn)
    old_book = books[book_id].model_dump()
    old_book.update(payload.model_dump(exclude_unset=True))
    new_book = Book(**old_book)
    books[book_id] = new_book 
    return books[book_id]

@app.delete("/books/{book_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int): 
    if book_id not in books: 
        raise BookNotFound(book_id)
    del books[book_id]