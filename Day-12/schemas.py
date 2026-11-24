from pydantic import BaseModel, ConfigDict , Field 
from datetime import date,datetime  
from enum import Enum 

class TodoCreate(BaseModel): 
    title: str = Field(min_length=3,max_length=100,examples=["Learn Websockets"])
    description: str | None = Field(max_length=500,default=None)
    due_date: date | None 


class TodoUpdate(BaseModel): 
    title: str | None = Field(min_length=3,max_length=100,default=None)
    description: str | None = Field(max_length=500,default=None)
    due_date: date | None = None 
    done: bool | None = None 

class TodoOut(BaseModel): 
    model_config = ConfigDict(from_attributes=True)
    id: int 
    title: str 
    description: str | None
    due_date: str  
    done: bool 
    created_at: datetime 
    updated_at: datetime 

class OrderBy(str,Enum):
    created_at = "created_at"
    title = "title"
    id = "id"
    due_date = "due_date"
    created_at = "created_at"
    updated_at = "updated_at"