from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from main.models.course import Course as DBCourse #Renamed as DBCourse for consistency's sake
from main.schema.lead import Lead,LeadBase,ShortLead, CourseAttempt
from main.models.lead import Lead as DBLead, CourseAttempt as DBAttempt


class LeadService:
    
    def list_leads(self,db:Session,skip:int,limit:int) -> List[ShortLead]:
        db_leads = db.query(DBLead).offset(skip).limit(limit).all()
        leads = [ShortLead(id=db_lead.id,name=db_lead.name,last_name=db_lead.last_name, carreer=db_lead.carreer) 
                for db_lead in db_leads]
        return leads
        
    def get_lead(self,db:Session,lead_id:int) -> Lead:
        db_lead:DBLead = db.query(DBLead).get(id)
        if not db_lead:
            return None
        
        attempts = []
        for attempt in db_lead.attempts:
            #TODO Research join
            course_name = db.query(DBCourse).get(attempt.course_id).name 
            attempts.append(CourseAttempt(course_name=course_name,attempt_year=attempt.year))

        lead = db_lead.to_dict()
        lead.pop('attempts',None)
        return Lead(**lead,attempts=attempts)

    def create_lead(self,db:Session, lead:LeadBase) -> Lead:
        attempts = lead.attempts
        lead_dict = lead.__dict__
        lead_dict.pop('attempts',None)
        db_lead = DBLead(**lead_dict)
        db.add(db_lead)
        try:
            db.commit()
        except IntegrityError:
            return None
        db.refresh(db_lead)
        for attempt in attempts:
            course = attempt.course_name.upper()
            db_course = db.query(DBCourse).filter(DBCourse.name==course).first() 
            # We create the course if it doesnt exist
            if db_course is None:
                db_course = DBCourse(name=course)
                db.add(db_course)
                db.commit()
                db.refresh(db_course)
            db_attempt = DBAttempt(lead_id = db_lead.id,course_id=db_course.id,attempt_year=attempt.attempt_year)
            db.add(db_attempt)
        db.commit()
        db.refresh(db_lead)
        lead_dict = db_lead.to_dict()
        lead_dict.attempts = attempts
        return Lead(**lead_dict)
    
    async def delete_lead(self,db:Session, id:int) -> bool:
        db_lead:DBLead = db.query(DBLead).get(id)
        if db_lead is None: 
            return False
        db.delete(db_lead)
        db.commit()  
        return True



lead_service = LeadService()