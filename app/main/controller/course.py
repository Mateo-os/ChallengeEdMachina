from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException, APIRouter, Depends, Query,status, responses

from database import get_db
from main.services.course import course_service
from main.schema.course import Course,CourseBase

router = APIRouter()

@router.get('/',response_model = List[Course])
async def list_courses(db:Session = Depends(get_db), skip: int = Query(0, description="Skip items", ge=0), 
                    limit: int = Query(10, description="Limit items", le=50)) -> List[Course]:
    return course_service.list_courses(db,skip,limit)

@router.post('/',response_model=Course)
def create_course(course:CourseBase, db:Session=Depends(get_db)) -> Course:
    course = course_service.create_course(db=db,course=course)
    if not course: 
         raise HTTPException(400,detail="Course with that name already exists")
    return course

@router.delete('/{id}',status_code=status.HTTP_200_OK)
def delete_course(id:int,db:Session = Depends(get_db)):
    if not course_service.delete_course(db,id):
        raise HTTPException(400,"Delete unsucessfull")
    return
