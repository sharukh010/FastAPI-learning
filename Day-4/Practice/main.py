from fastapi import FastAPI 
from models import StudentCreate, Student , StudentOut

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