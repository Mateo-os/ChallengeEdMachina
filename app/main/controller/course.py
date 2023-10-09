from typing import List
from app.database import get_db
from sqlalchemy.orm import Session
from fastapi import HTTPException, APIRouter, Depends, Query

from services.course import course_service
from schema.course import Course,CourseBase

router = APIRouter()

@router.get('/courses/',response_model = List[Course])
async def list_courses(db:Session = Depends(get_db), skip: int = Query(0, description="Skip items", ge=0), 
                    limit: int = Query(10, description="Limit items", le=50)) -> List[Course]:
    return course_service.list_courses(db,skip,limit)

@router.post('/courses/',response_model=Course)
def create_course(course:CourseBase, db:Session=Depends(get_db)) -> Course:
    course = course_service.create_course(db=db,course=course)
    if not course: 
         raise HTTPException(400,detail="Course with that name already exists")
    return course


