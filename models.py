from sqlalchemy import Column, Integer, String,LargeBinary
from database import Base

#Database model
class Student(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    gender = Column(String)
    branch = Column(String)
    year = Column(String)
    image = Column(LargeBinary)
