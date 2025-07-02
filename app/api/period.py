from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from app import models, schemas
from app.db import get_db

router = APIRouter()

@router.get("/periods", response_model=List[schemas.Period])
def get_periods(user_name: str = Query(...), db: Session = Depends(get_db)):
    return db.query(models.Period).filter(models.Period.user_name == user_name).all()

@router.post("/periods", response_model=schemas.Period)
def create_period(period: schemas.PeriodCreate, db: Session = Depends(get_db)):
    db_period = models.Period(**period.dict())
    db.add(db_period)
    db.commit()
    db.refresh(db_period)
    return db_period

@router.delete("/periods/{period_id}")
def delete_period(period_id: int, db: Session = Depends(get_db)):
    period = db.query(models.Period).filter(models.Period.id == period_id).first()
    if not period:
        raise HTTPException(status_code=404, detail="Period not found")
    db.delete(period)
    db.commit()
    return {"message": "Period deleted"}