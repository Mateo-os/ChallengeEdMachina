
from typing import List, Annotated
from fastapi import FastAPI,Depends, Query, HTTPException
import dbmodels
import models

from database import engine, session
from sqlalchemy.orm import Session

app = FastAPI()
dbmodels.Base.metadata.create_all(bind=engine)


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]




@app.get('/')
async def root():
    return {'message': 'Too Lazy to make a front, post the lead at the /leads/ endpoint'}


@app.get('/leads/',response_model = List[models.ShortLead])
async def get_leads(db:db_dependency, skip: int = Query(0, description="Skip items", ge=0), 
                    limit: int = Query(10, description="Limit items", le=50)):
    db_leads = db.query(dbmodels.Lead).offset(skip).limit(limit).all()
    leads = [models.ShortLead(id=db_lead.id,name=db_lead.name,last_name=db_lead.last_name, carreer=db_lead.carreer) 
             for db_lead in db_leads]
    return leads

@app.get('/leads/{id}',response_model=models.Lead)
async def get_lead(id:int,db:db_dependency):
    db_lead:dbmodels.Lead = db.query(dbmodels.Lead).get(id)
    if db_lead is None: raise HTTPException(404)
    db_attempts = db.query(dbmodels.CourseAttempt).filter(dbmodels.CourseAttempt.lead_id == id).all()
    attempts = []
    for attempt in db_attempts:
        course_name = db.query(dbmodels.Course).get(attempt.course_id).name
        attempts.append(models.CourseAttempt(course_name=course_name,attempt_year=attempt.attempt_year))
    
    lead = models.Lead(
        id=db_lead.id,name=db_lead.name,last_name=db_lead.last_name,
        email=db_lead.email,registration_year=db_lead.registration_year,
        phone=db_lead.phone,carreer=db_lead.carreer,attempts=attempts
    )
    return lead


@app.post('/leads/',response_model=models.Lead)
async def create_lead(lead:models.Lead,db:db_dependency):
    l_dict = lead.__dict__.copy()
    l_dict.pop('id',None)
    attempts:List[models.CourseAttempt] = l_dict.pop('attempts',[])
    db_lead = dbmodels.Lead(**l_dict)
    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)
    for attempt in attempts:
        course = attempt.course_name.upper()
        db_course = db.query(dbmodels.Course).filter(dbmodels.Course.name==course).first() 
        # We create the course if it doesnt exist
        if db_course is None:
            db_course = dbmodels.Course(name=course)
            db.add(db_course)
            db.commit()
            db.refresh(db_course)
        db_attempt = dbmodels.CourseAttempt(lead_id = db_lead.id,course_id=db_course.id,attempt_year=attempt.attempt_year)
        db.add(db_attempt)
    db.commit()
    lead.id = db_lead.id
    return lead


@app.delete('/leads/{id}')
async def delete_lead(id,db:db_dependency):
    db_lead:dbmodels.Lead = db.query(dbmodels.Lead).get(id)
    if db_lead is None: raise HTTPException(404)
    db.delete(db_lead)
    db.commit()  

@app.post('/courses/',response_model=models.Course)
async def create_course(course:models.Course,db:db_dependency):
    course.name = course.name.upper()
    db_course = db.query(dbmodels.Course).filter(dbmodels.Course.name==course.name).first()
    if db_course is not None:
        raise HTTPException(409,detail="Course with that name already exists")
    course_dict = course.__dict__.copy()
    course_dict.pop('id',None)
    db_course = dbmodels.Course(**course_dict)
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    course.id = db_course.id
    return course

@app.get('/courses/',response_model = List[models.Course])
async def get_courses(db:db_dependency, skip: int = Query(0, description="Skip items", ge=0), 
                    limit: int = Query(10, description="Limit items", le=50)):
    db_courses = db.query(dbmodels.Course).offset(skip).limit(limit).all()
    courses = [models.Course(id=db_course.id,name=db_course.name) 
             for db_course in db_courses]
    return courses



@app.delete('/courses/{id}')
async def delete_course(id,db:db_dependency):
    db_course:dbmodels.Course = db.query(dbmodels.Course).get(id)
    if db_course is None: raise HTTPException(404)
    db.delete(db_course)
    db.commit()  
