from pydantic import BaseModel, Field, EmailStr, field_validator,model_validator
from fastapi import FastAPI 

class Address(BaseModel): 
    city: str 
    pincode: str = Field(pattern=r"^\d{6}$")

class UserCreate(BaseModel): 
    username: str = Field(min_length=3,max_length=20,pattern=r"^[a-zA-Z0-9_]+$")
    email: EmailStr 
    password: str = Field(min_length=8)
    age: int = Field(ge=13,le=120)
    confirm_password: str 
    address: Address | None = None 

    @field_validator("password")
    @classmethod
    def strong_password(cls,v): 
        if not any(c.isdigit() for c in v): 
            raise ValueError("Password must contain a digit")
        return v 

    @model_validator(mode="after")
    def password_match(self): 
        if self.password != self.confirm_password: 
            raise ValueError("Passwords do not match")
        return self 

class UserOut(BaseModel): 
    id: int 
    username: str 
    email: EmailStr 
    address: Address | None = None 

users : list[dict] = [] 
next_id = 1 
app = FastAPI()

@app.post("/register",response_model=UserOut,status_code=201)
def register(user: UserCreate): 
    global next_id 
    new = user.model_dump(exclude={"confirm_password"})
    new["id"] = next_id 
    next_id += 1 
    users.append(new)
    return new 