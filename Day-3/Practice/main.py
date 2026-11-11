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

@app.get("/health")
def health(): 
    return {"status": "ok"}