from enum import Enum 
from pydantic import BaseModel,Field 
from datetime import datetime 

class Priority(str,Enum): 
    low = "low"
    medium = "medium"
    high = "high"

class SortBy(str,Enum): 
    created_at = "created_at"
    due_date = "due_date"
    priority = "priority"
    title = "title"

class SortOrder(str,Enum): 
    asc = "asc"
    desc = "desc"

class TodoCreate(BaseModel):
    title: str = Field(min_length=1,max_length=100,examples=["Practice FastAPI"])
    description: str | None = Field(default=None,max_length=500,examples=["Do the Todo API Project"])
    completed: bool = Field(default=False,examples=[True]) 
    priority: Priority = Field(default=Priority.medium,examples=[Priority.low,Priority.high])
    due_date: str | None  = Field(default=None,pattern=r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$",examples=["2026-11-20"])


class TodoPatch(BaseModel): 
    title: str | None  = Field(default=None,min_length=1,max_length=100)
    description: str | None = Field(default=None,max_length=500)
    completed: bool | None  = None  
    priority: Priority | None = None 
    due_date: str | None = Field(default=None,pattern=r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$")

class Todo(TodoCreate): 
    id: int 
    created_at: datetime
    updated_at: datetime 


class StatsResponse(BaseModel): 
    total : int 
    completed: int 
    pending: int 
    overdue: int 
    by_priority: dict[str,int]