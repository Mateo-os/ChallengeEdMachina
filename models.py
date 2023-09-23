from pydantic import BaseModel
from typing import List, Optional


class Course(BaseModel):
    id : Optional[int] = None
    name:str

class CourseAttempt(BaseModel):
    course_name:str
    attempt_year:int


class Lead(BaseModel):
    id: Optional[int] = None
    name: str
    last_name: str
    email:Optional[str] = ""
    phone:Optional[str] = ""
    carreer: str
    registration_year: int
    attempts: Optional[List[CourseAttempt]] = None 

class ShortLead(BaseModel):
    id:int
    name: str
    last_name: str
    carreer: str
    