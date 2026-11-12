from fastapi import FastAPI, Path, HTTPException
from models import StudentCreate, Student , StudentOut , Course 
from typing import Annotated

app = FastAPI()

students: list[Student] = []
next_id = 1 

@app.post("/students",response_model=StudentOut)
def create_student(payload: StudentCreate): 
    global next_id 
    student = Student(id=next_id,**payload.model_dump(exclude={"confirm_password"}))
    next_id += 1 
    students.append(student)
    return student

@app.get("/students",response_model=list[StudentOut])
def list_students(course: Course | None = None):
    results = students 
    if course is None: 
        return results 
    else: 
        results = [s for s in results if s.course == course]
    return results  

@app.get("/students/{student_id}",response_model=StudentOut)
def get_student(student_id: Annotated[int,Path(ge=1)]): 
    student = None 
    for s in students: 
        if s.id == student_id: 
            student = s 
            break 
    if student is None: 
        raise HTTPException(status_code=404,detail="Student not found")
    return student 