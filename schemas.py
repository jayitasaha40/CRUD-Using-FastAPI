from fastapi import UploadFile
from pydantic import BaseModel,validator
from typing import Optional

from enum import Enum


# Enum for Gender
class Gender(str, Enum):
    male = "Male"
    female = "Female"
    other = "Other"

# Enum for Branch
class Branch(str, Enum):
    cse = "CSE"
    ece = "ECE"
    ee = "EE"
    me = "ME"
    ce = "CE"

# Pydantic model for request data
class StudentCreate(BaseModel):
    name: str
    gender: Gender
    branch: Branch
    year: int

    @validator('year')
    def validate_year(cls, value):
        if value < 1995 or value > 2028:  
            raise ValueError('Year must be between 1995 and 2028')
        return value

# Pydantic model for response data
class StudentResponse(BaseModel):
    id: int
    name: str
    gender: str
    branch: str
    year: int

    class Config:
        orm_mode = True



class StudentUpdate(BaseModel):
    name: Optional[str]
    branch: Optional[Branch]
   

    class Config:
        orm_mode = True
