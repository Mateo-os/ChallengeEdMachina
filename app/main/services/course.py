from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models.course import Course as DBCourse
from schema.course import Course,CourseBase

class CourseService:
    
    def list_courses(db:Session,skip:int,limit:int) -> List[Course]:
        db_courses = db.query(DBCourse).offset(skip).limit(limit).all()
        courses = [Course(c.to_dict()) for c in db_courses]
        return courses 

    def create_course(db:Session, course:CourseBase) -> Course:
        course.name = course.name.upper()
        db_course = DBCourse(**course.__dict__)
        db.add(db_course)
        try:
            db.commit()
        except IntegrityError:
            return None
        db.refresh(db_course)
        return Course(db_course.to_dict())
    
course_service = CourseService()