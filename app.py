# Import necessary modules and classes
from typing import List
from fastapi import FastAPI, Depends, HTTPException, File, Response, UploadFile
from sqlalchemy import create_engine, Column, Integer, String, LargeBinary
import sqlalchemy
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel

# FastAPI app instance
app = FastAPI()

# Database setup
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = sqlalchemy.orm.declarative_base()

# Database model
class Student(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    gender = Column(String)
    branch = Column(String)
    year = Column(String)
    image = Column(LargeBinary)

# Create tables
Base.metadata.create_all(bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
