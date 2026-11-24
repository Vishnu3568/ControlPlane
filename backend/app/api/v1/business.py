from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from backend.app.core.database import get_db
from backend.app.services.business_service import BusinessService
from backend.app.schemas.business import (
    BusinessOpportunityCreate, BusinessOpportunityUpdate, BusinessOpportunityResponse,
    ExperimentCreate, ExperimentUpdate, ExperimentResponse
)

router = APIRouter(prefix="/business", tags=["Business Lab"])

@router.get("/opportunities", response_model=List[BusinessOpportunityResponse])
def get_opportunities(db: Session = Depends(get_db)):
    return BusinessService.get_opportunities(db)

@router.post("/opportunities", response_model=BusinessOpportunityResponse, status_code=status.HTTP_201_CREATED)
def create_opportunity(data: BusinessOpportunityCreate, db: Session = Depends(get_db)):
    return BusinessService.create_opportunity(db, data)

@router.get("/opportunities/{opp_id}", response_model=BusinessOpportunityResponse)
def get_opportunity(opp_id: int, db: Session = Depends(get_db)):
    opp = BusinessService.get_opportunity_by_id(db, opp_id)
    if not opp:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    return opp

@router.put("/opportunities/{opp_id}", response_model=BusinessOpportunityResponse)
def update_opportunity(opp_id: int, data: BusinessOpportunityUpdate, db: Session = Depends(get_db)):
    opp = BusinessService.update_opportunity(db, opp_id, data)
    if not opp:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    return opp

@router.delete("/opportunities/{opp_id}")
def delete_opportunity(opp_id: int, db: Session = Depends(get_db)):
    success = BusinessService.delete_opportunity(db, opp_id)
    if not success:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    return {"message": "Opportunity deleted successfully"}

# --- EXPERIMENTS ---
@router.post("/experiments", response_model=ExperimentResponse, status_code=status.HTTP_201_CREATED)
def create_experiment(data: ExperimentCreate, db: Session = Depends(get_db)):
    return BusinessService.create_experiment(db, data)

@router.put("/experiments/{exp_id}", response_model=ExperimentResponse)
def update_experiment(exp_id: int, data: ExperimentUpdate, db: Session = Depends(get_db)):
    exp = BusinessService.update_experiment(db, exp_id, data)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.delete("/experiments/{exp_id}")
def delete_experiment(exp_id: int, db: Session = Depends(get_db)):
    success = BusinessService.delete_experiment(db, exp_id)
    if not success:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return {"message": "Experiment deleted successfully"}

