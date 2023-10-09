from typing import List
from app.database import get_db
from sqlalchemy.orm import Session
from fastapi import HTTPException, APIRouter, Depends, Query

from services.lead import lead_service
from schema.lead import Lead, LeadBase, ShortLead

router = APIRouter()

@router.get('/leads/',response_model = List[ShortLead])
async def get_leads(db:Session= Depends(get_db), skip: int = Query(0, description="Skip items", ge=0), 
                    limit: int = Query(10, description="Limit items", le=50)) -> List[ShortLead]:
    return lead_service.list_leads(db,skip,limit)

@router.get('/leads/{id}',response_model=Lead)
def get_lead(id:int, db:Session = Depends(get_db)):
    lead = lead_service.get_lead(db,id)
    if not lead:
        raise HTTPException(404,"Does not exist")
    return lead

@router.post('/leads/',response_model=Lead)
def create_lead(base_lead:LeadBase, db:Session = Depends(get_db)):
    lead = lead_service.create_lead(db = db, lead=base_lead)
    if not lead:
        raise HTTPException(400)
    return lead
