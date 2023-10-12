from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from main.models.course import Course as DBCourse
from main.schema.course import Course, CourseBase
from .base import BaseService


class CourseService(BaseService):
    def list_courses(self, db: Session, skip: int, limit: int) -> List[Course]:
        db_courses = db.query(DBCourse).offset(skip).limit(limit).all()
        courses = [Course(**c.to_dict()) for c in db_courses]
        return courses

    def create_course(self, db: Session, course: CourseBase) -> Course:
        course.name = course.name.upper()
        db_course = DBCourse(**course.__dict__)
        db.add(db_course)
        try:
            db.commit()
        except IntegrityError:
            return None
        db.refresh(db_course)
        return Course(**db_course.to_dict())

    def delete_course(self, db: Session, id: int) -> bool:
        db_course: DBCourse = db.query(DBCourse).get(id)
        if db_course is None:
            return False
        db.delete(db_course)
        db.commit()
        return True


course_service = CourseService()
