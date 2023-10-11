from pydantic import BaseModel
from typing import List, Optional


class CourseAttempt(BaseModel):
    course_name:str
    attempt_year:int

class LeadBase(BaseModel):
    name: str
    last_name: str
    email:Optional[str] = ""
    phone:Optional[str] = ""
    carreer: str
    registration_year: int
    attempts: Optional[List[CourseAttempt]] = None 

class Lead(LeadBase):
    id: Optional[int] = None
        
    class Config: 
        orm_mode = True

#Models for Leads, with reduced information
class ShortLead(BaseModel):
    id:int
    name: str
    last_name: str
    carreer: str



    

