from fastapi import FastAPI , HTTPException,status,Query
from pydantic import BaseModel, Field 
from datetime import datetime
from typing import Annotated
from zoneinfo import ZoneInfo

zone = "Asia/Kolkata"

app = FastAPI(title="Notes API")

class NoteCreate(BaseModel): 
    title: str | None = Field(default=None,min_length=1,max_length=100,examples=["Practice FastAPI"])
    content: str | None = Field(default=None,examples=["Practice Day-5"])
    created_at: datetime | None = None 

class NoteUpdate(BaseModel): 
    title: str | None = Field(default=None,min_length=1,max_length=100,examples=["Practice FastAPI"])
    content: str | None = Field(default=None,examples=["Practice Day-5"])
    updated_at: datetime | None = None 

class Note(NoteCreate): 
    id: int 
    created_at: datetime
    updated_at: datetime | None = None 

notes: dict[int,Note] = {}
next_id = 1 

def get_or_404(note_id: int | None = None)-> Note: 
    note = notes.get(note_id)
    if note is None: 
        raise HTTPException(status_code=404,detail="Note not found")
    return note 

@app.post("/notes",response_model=Note,status_code=status.HTTP_201_CREATED)
def create_note(data: NoteCreate): 
    global next_id 
    note = Note(id=next_id,**data.model_dump(exclude={"created_at"}),created_at=data.created_at or datetime.now(ZoneInfo(zone)))
    notes[next_id] = note 
    next_id += 1 
    return note  

@app.get("/notes",response_model=list[Note])
def list_notes(
    search: Annotated[str | None,Query(min_length=1,max_length=100)] = None
    ): 
    result = list(notes.values())
    if search is None: 
        return result 
    result = [n for n in result if search.lower() in n.title.lower()]
    
    return result

@app.get("/notes/{note_id}",response_model=Note)
def read_note(note_id: int):
    return get_or_404(note_id)

@app.put("/notes/{note_id}",response_model=Note)
def replace_note(note_id: int, data: NoteCreate): 
    get_or_404(note_id)
    note = Note(id=note_id,**data.model_dump(exclude={"created_at"}),created_at= data.created_at or datetime.now(ZoneInfo(zone)),updated_at= datetime.now(ZoneInfo(zone)))
    notes[note_id] = note 
    return note 

@app.patch("/notes/{note_id}",response_model=Note)
def update_note(note_id: int, data: NoteUpdate): 
    note = get_or_404(note_id)
    changes = data.model_dump(exclude_unset=True)
    updated = note.model_copy(update=changes)
    updated.updated_at = data.updated_at or datetime.now(ZoneInfo(zone))
    notes[note_id] = updated 
    return updated 

@app.delete("/notes/{note_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_note(note_id: int): 
    get_or_404(note_id)
    del notes[note_id]