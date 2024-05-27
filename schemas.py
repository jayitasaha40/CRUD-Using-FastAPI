from fastapi import UploadFile
from pydantic import BaseModel
from typing import Optional

# Pydantic model for request data
class StudentCreate(BaseModel):
    name: str
    gender: str
    branch: str
    year: str

# Pydantic model for response data
class StudentResponse(BaseModel):
    id: int
    name: str
    gender: str
    branch: str
    year: str

    class Config:
        orm_mode = True



class StudentUpdate(BaseModel):
    name: Optional[str]
    gender: Optional[str]
    branch: Optional[str]
    year: Optional[str]

    class Config:
        orm_mode = True