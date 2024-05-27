# Import necessary modules and classes
from typing import List, Optional
from fastapi import FastAPI, Depends, Form, HTTPException, File, Response, UploadFile
from sqlalchemy import create_engine, Column, Integer, String, LargeBinary
import sqlalchemy
from sqlalchemy.orm import sessionmaker, Session
from database import engine, Base, get_db
from models import Student
from schemas import StudentCreate, StudentResponse, StudentUpdate

# FastAPI app instance
app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)



# Pydantic model for request data


# # Pydantic model for a list of students
# class StudentListResponse(BaseModel):
#     students: list[StudentResponse]

# API endpoint to create a student with an image
@app.post("/students/", response_model=StudentResponse)
async def create_student(
    name: str,
    gender: str,
    branch: str,
    year: str,
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    image_data = await image.read()
    db_student = Student(
        name=name,
        gender=gender,
        branch=branch,
        year=year,
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
    name: Optional[str] = Form(None),
    gender: Optional[str] = Form(None),
    branch: Optional[str] = Form(None),
    year: Optional[str] = Form(None),
    image: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    
    if name is not None:
        db_student.name = name
    if gender is not None:
        db_student.gender = gender
    if branch is not None:
        db_student.branch = branch
    if year is not None:
        db_student.year = year
    if image is not None:
        image_data = await image.read()
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
