from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database import db
from .base import BaseModel

class Lead(db.Model,BaseModel):
    __tablename__ = "leads"
    id = Column(Integer,primary_key=True, index=True)
    name = Column(String,default="")
    last_name = Column(String,index=True,default="")
    email = Column(String,index=True,default="") 
    phone = Column(String,default="") # Phone will be a string for now because its easier to handle 
    carreer = Column(String,index=True,default="")
    registration_year = Column(Integer,default=0)
    attempts = relationship('CourseAttempt', backref='lead', passive_deletes=True)

# Save the relation as a separate table to make it easier to countabilize
class CourseAttempt(db.Model,BaseModel):
    __tablename__ = "attempts"
    lead_id = Column(Integer,ForeignKey("leads.id",ondelete="CASCADE"),primary_key=True)
    course_id = Column(Integer,ForeignKey("courses.id",ondelete="CASCADE"),primary_key=True)
    attempt_year = Column(Integer)


    