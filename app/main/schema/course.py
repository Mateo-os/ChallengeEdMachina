from typing import List, Optional
from pydantic import BaseModel

#right now this models is useless/redundant but is good future-proofing
class CourseBase(BaseModel):
    name:str

class Course(CourseBase):
    id: int

    class Config:
        orm_mode = True
