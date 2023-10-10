from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Integer, String
from database import db
from .base import BaseModel

class Course(db.Model,BaseModel):
    __tablename__ = "courses"
    id = Column(Integer,primary_key=True, autoincrement=True,index=True)
    name = Column(String,unique=True)
    attempts = relationship('CourseAttempt', backref='course', passive_deletes=True)
   
    
