from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from backend.app.models.business import BusinessOpportunity, Experiment
from backend.app.schemas.business import (
    BusinessOpportunityCreate, BusinessOpportunityUpdate,
    ExperimentCreate, ExperimentUpdate
)

class BusinessService:
    @staticmethod
    def get_opportunities(db: Session) -> List[BusinessOpportunity]:
        return db.query(BusinessOpportunity).order_by(BusinessOpportunity.updated_at.desc()).all()

    @staticmethod
    def get_opportunity_by_id(db: Session, opp_id: int) -> Optional[BusinessOpportunity]:
        return db.query(BusinessOpportunity).filter(BusinessOpportunity.id == opp_id).first()

    @staticmethod
    def create_opportunity(db: Session, data: BusinessOpportunityCreate) -> BusinessOpportunity:
        opp = BusinessOpportunity(**data.model_dump())
        db.add(opp)
        db.commit()
        db.refresh(opp)
        return opp

    @staticmethod
    def update_opportunity(db: Session, opp_id: int, data: BusinessOpportunityUpdate) -> Optional[BusinessOpportunity]:
        opp = db.query(BusinessOpportunity).filter(BusinessOpportunity.id == opp_id).first()
        if not opp:
            return None
        for key, val in data.model_dump(exclude_unset=True).items():
            setattr(opp, key, val)
        db.commit()
        db.refresh(opp)
        return opp

    @staticmethod
    def delete_opportunity(db: Session, opp_id: int) -> bool:
        opp = db.query(BusinessOpportunity).filter(BusinessOpportunity.id == opp_id).first()
        if not opp:
            return False
        db.delete(opp)
        db.commit()
        return True

    @staticmethod
    def create_experiment(db: Session, data: ExperimentCreate) -> Experiment:
        exp = Experiment(**data.model_dump())
        if not exp.start_date:
            exp.start_date = date.today()
        db.add(exp)
        db.commit()
        db.refresh(exp)
        return exp

    @staticmethod
    def update_experiment(db: Session, exp_id: int, data: ExperimentUpdate) -> Optional[Experiment]:
        exp = db.query(Experiment).filter(Experiment.id == exp_id).first()
        if not exp:
            return None
        for key, val in data.model_dump(exclude_unset=True).items():
            setattr(exp, key, val)
        db.commit()
        db.refresh(exp)
        return exp

    @staticmethod
    def delete_experiment(db: Session, exp_id: int) -> bool:
        exp = db.query(Experiment).filter(Experiment.id == exp_id).first()
        if not exp:
            return False
        db.delete(exp)
        db.commit()
        return True

