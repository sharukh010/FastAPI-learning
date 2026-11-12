from pydantic import BaseModel,Field,EmailStr,field_validator,model_validator
from enum import Enum 

class Course(str,Enum):
    python = "python"
    ap_cs = "ap_cs"
    gcse = "gcse"

class Address(BaseModel): 
    city: str = Field(min_length=2,max_length=50,examples=["Vijayawada","Hyderabad"])
    state: str = Field(min_length=3,examples=["Andhra Pradesh","Telengana"])
    pincode: str = Field(pattern=r"\d{6}$",examples=["520013","500001"])

class StudentCreate(BaseModel): 
    name: str = Field(min_length=3,max_length=50,pattern=r"^[A-Za-z ]+$",examples=["sharukh khan","salman khan"])
    bio: str | None= Field(default=None,max_length=200,examples="I am a studying CS Major")
    email: EmailStr = Field(examples=["sharukh@example.com","salman@example.com"])
    phone: str = Field(pattern=r"^[6-9]\d{9}$",examples=["9876543231"])
    age: int = Field(ge=10,le=60,examples=[15,19])
    course: Course 
    password: str = Field(examples=["hello123","Hello@01"])
    confirm_password: str = Field(examples=["hello123","Hello@01"])
    address: Address
    guardian_email: EmailStr | None = Field(default=None,examples=["amitabachan@example.com","amirkhan@example.com",None])

    @field_validator("password")
    @classmethod
    def strong_password(cls,v): 
        if not any(c.isupper() for c in v): 
            raise ValueError("Password must contain Upper case characters")
        elif not any(c.isdigit() for c in v): 
            raise ValueError("Password must contain atleast one digit")
        elif not any((c in "!@#$%^&*()_+-=[];:'|,.<>/?~") for c in v): 
            raise ValueError("Password must contain atleast one special character")
        return v 

    @field_validator("name")
    @classmethod
    def clean_name(cls,v): 
        v = v.strip().title()
        return v 
    
    @model_validator(mode="after")
    def password_match(self): 
        if self.password != self.confirm_password: 
            raise ValueError("Passwords do not match")
        return self 

    @model_validator(mode="after")
    def age_verification(self): 
        if self.age < 18 and self.guardian_email is None:
            raise ValueError("Below 18 age requires to enter gaurdian email")
        return self  

class Student(BaseModel):
    id: int 
    name: str = Field(min_length=3,max_length=50,pattern=r"^[A-Za-z ]+$")
    bio: str | None= Field(default=None,max_length=200,examples="I am a studying CS Major")
    email: EmailStr 
    phone: str = Field(pattern=r"^[6-9]\d{9}$")
    age: int = Field(ge=10,le=60)
    course: Course 
    password: str
    address: Address
    guardian_email: EmailStr | None = None 

class StudentOut(BaseModel): 
    id: int 
    name: str = Field(min_length=3,max_length=50,pattern=r"^[A-Za-z ]+$")
    email: EmailStr 
    course: Course 
    address: Address 