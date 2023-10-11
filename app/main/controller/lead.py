from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException, APIRouter, Depends, Query, status

from database import get_db
from main.services.lead import lead_service
from main.schema.lead import Lead, LeadBase, ShortLead
router = APIRouter()

@router.get('/',response_model = List[ShortLead])
async def get_leads(db:Session= Depends(get_db), skip: int = Query(0, description="Skip items", ge=0), 
                    limit: int = Query(10, description="Limit items", le=50)) -> List[ShortLead]:
    ls = lead_service.list_leads(db,skip,limit)
    return lead_service.list_leads(db,skip,limit)

@router.get('/{id}',response_model=Lead)
async def get_lead(id:int, db:Session = Depends(get_db)):
    lead = lead_service.get_lead(db,id)
    if not lead:
        raise HTTPException(404,"Does not exist")
    return lead

@router.post('/',response_model=Lead)
def create_lead(base_lead:LeadBase, db:Session = Depends(get_db)):
    lead = lead_service.create_lead(db = db, lead=base_lead)
    if not lead:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    return lead

@router.delete('/{id}')
async def delete_lead(id:int,db:Session = Depends(get_db),status_code=status.HTTP_200_OK):
    if not lead_service.delete_lead(db=db,id=id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    return