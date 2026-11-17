from enum import Enum 
from pydantic import BaseModel,Field 
from datetime import datetime 

class Priority(str,Enum): 
    low = "low"
    medium = "medium"
    high = "high"

class TodoCreate(BaseModel):
    title: str = Field(min_length=1,max_length=100)
    description: str | None = Field(default=None,max_length=500)
    completed: bool = False 
    priority: Priority = Priority.medium
    due_date: str 


class TodoPatch(BaseModel): 
    title: str | None  = Field(default=None,min_length=1,max_length=100)
    description: str | None = Field(default=None,max_length=500)
    completed: bool | None  = None  
    priority: Priority | None = None 
    due_date: str | None = None 

class Todo(TodoCreate): 
    id: int 
    created_at: datetime
    updated_at: datetime 


class StatsResponse(BaseModel): 
    total : int 
    completed: int 
    pending: int 
    overdue: int 
    by_priority: dict[str]