from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Integer, String

from .base import BaseModel

class Course(BaseModel):
    __tablename__ = "courses"
    id = Column(Integer,primary_key=True, autoincrement=True,index=True)
    name = Column(String,unique=True,index=True)
    attempts = relationship('CourseAttempt', backref='course', passive_deletes=True)
   
    
