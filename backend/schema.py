from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

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

class JobUpdate(BaseModel):
    type: Optional[str]
    title: Optional[str] 
    description: Optional[str]
    min_experience: Optional[int]
    max_experience: Optional[int]
    location: Optional[str] 
    mode: Optional[str]
    compensation: Optional[int]
    compensation_type: Optional[str]
    is_open: Optional[bool]

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
