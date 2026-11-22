from pydantic import BaseModel, ConfigDict 

class TodoCreate(BaseModel): 
    title: str 
    description: str | None = None 

class TodoOut(TodoCreate): 
    id: int 
    done: bool 
    model_config = ConfigDict(from_attributes=True)