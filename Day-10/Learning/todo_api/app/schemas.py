from pydantic import BaseModel, Field 
from zoneinfo import ZoneInfo
from datetime import datetime 
from uuid import UUID
zone = ZoneInfo("Asia/Kolkata")


class TodoCreate(BaseModel): 
    title: str = Field(min_length=3,max_length=200,examples=["Learn FastAPI"])
    description: str | None = Field(default=None)
    completed: bool = False 


class Todo(TodoCreate): 
    id: UUID
    created_at: datetime 
    updated_at: datetime 