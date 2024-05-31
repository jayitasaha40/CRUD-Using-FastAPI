# Import necessary modules and classes
from typing import List, Optional
from fastapi import FastAPI, Depends, Form, HTTPException, File, Response, UploadFile
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from sqlalchemy import create_engine, Column, Integer, String, LargeBinary
import sqlalchemy
from sqlalchemy.orm import sessionmaker, Session
from database import engine, Base, get_db
from models import Student
from schemas import StudentCreate, StudentResponse, StudentUpdate,Gender,Branch
from enum import Enum
import logging
from pydantic.error_wrappers import ValidationError as PydanticValidationError
import face_recognition

# FastAPI app instance
app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)




@app.post("/students/", response_model=StudentResponse)
async def create_student(
    name: str = Form(...),
    gender: Gender = Form(...),
    branch: Branch = Form(...),
    year: int = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        # Validate using Pydantic model
        student_data = StudentCreate(name=name, gender=gender, branch=branch, year=year)
    except ValueError as e:
        logger.error("Validation error:", exc_info=e)
        raise HTTPException(status_code=422, detail=str(e)) 
    image_data = await image.read()
    with open("saved_image.jpg", "wb") as f:
        f.write(image_data)

    image = face_recognition.load_image_file("saved_image.jpg")
    face_locations = face_recognition.face_locations(image)
    if(len(face_locations)<=0):
        raise HTTPException(status_code=422, detail="Face is not visible in the image") 
    db_student = Student(
        name=student_data.name,
        gender=student_data.gender.value,
        branch=student_data.branch.value,
        year=student_data.year,
        image=image_data
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


# API endpoint to get student list
@app.get("/studentlist/", response_model=List[StudentResponse])
async def read_studentlist(db: Session = Depends(get_db)):
    db_student = db.query(Student).all()
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student


# API endpoint to read a student by ID
@app.get("/students/{student_id}", response_model=StudentResponse)
async def read_student(student_id: int, db: Session = Depends(get_db)):
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student

# Endpoint to retrieve a student's image
@app.get("/students/{student_id}/image")
async def get_student_image(student_id: int, db: Session = Depends(get_db)):
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return Response(content=db_student.image, media_type="image/png")

#DELETE
@app.delete("/studentdelete/{student_id}", response_model=StudentResponse)
async def delete_student(student_id: int, db: Session = Depends(get_db)):
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    db.delete(db_student)
    db.commit()
    return db_student

#UPDATE
@app.put("/students/{student_id}", response_model=StudentResponse)
async def update_student(
    student_id: int,
    branch: Branch = Form(None),
    image: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    
   
    if branch is not None:
        db_student.branch = branch
    if image is not None:
        image_data = await image.read()
        with open("saved_image.jpg", "wb") as f:
            f.write(image_data)

        image = face_recognition.load_image_file("saved_image.jpg")
        face_locations = face_recognition.face_locations(image)
        if(len(face_locations)<=0):
            raise HTTPException(status_code=422, detail="Face is not visible in the image") 
        db_student.image = image_data
    
    db.commit()
    db.refresh(db_student)
    return db_student



@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)