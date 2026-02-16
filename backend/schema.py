from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime #, date

class JobCreate(BaseModel):
    type: str 
    title: str 
    description: str
    min_experience: int
    max_experience: int
    location: str 
    mode: str 
    compensation: int
    compensation_type: str 
    is_open: bool = True

# class JobUpdate(BaseModel):
#     type: Optional[str]
#     title: Optional[str] 
#     description: Optional[str]
#     min_experience: Optional[int]
#     max_experience: Optional[int]
#     location: Optional[str] 
#     mode: Optional[str]
#     compensation: Optional[int]
#     compensation_type: Optional[str]
#     is_open: Optional[bool]

class JobUpdate(BaseModel):
    type: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    min_experience: Optional[int] = None
    max_experience: Optional[int] = None
    location: Optional[str] = None
    mode: Optional[str] = None
    compensation: Optional[int] = None
    compensation_type: Optional[str] = None
    is_open: Optional[bool] = None
    class Config:
        from_attributes = True
        # extra = "forbid"

class JobResponse(BaseModel):
    id: int
    type: str
    title: str
    description: str
    min_experience: int
    max_experience: int
    location: str
    mode: str
    compensation: int
    compensation_type: str
    is_open: bool
    created_at: datetime
    
    # def format_created_at(self, value: datetime):
    #     return value.strftime("%d-%m-%Y %I:%M %p")

    class Config:
        from_attributes = True



class AdminCreate(BaseModel):
    name : str
    email : EmailStr
    password : str


class AdminLogin(BaseModel):
    email : EmailStr
    password : str


class AdminResponse(BaseModel):
    id : int
    name : str
    email : EmailStr
    level : str

    class Config:
        from_attributes = True

class AdminLoginResponse(BaseModel): 
    message: str
    access_token: str
    token_type: str

class ApplicantCreate(BaseModel):
    name : str
    email : EmailStr
    resume_url : str
    phone_no : int    #string if not work  phone_no: constr(pattern=r'^(\+91)?[0-9]{10}$')

class ApplicantAdminView(BaseModel):
    id: int
    job_id: int
    name: str
    email: EmailStr
    phone_no: int   #str
    resume_url: str
    applied_at: datetime

    class Config:
        from_attributes = True