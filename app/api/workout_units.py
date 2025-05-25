from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app import models, schemas
from app.db import get_db

router = APIRouter()

# =========================
# WorkoutUnit Endpoints
# =========================

@router.get("/workout_units", response_model=List[schemas.WorkoutUnit])
def read_workout_units(
    user_name: str = Query(..., description="Username to filter units by"), 
    workout_id: Optional[int] = Query(None, description="Workout ID to filter units by"), 
    db: Session = Depends(get_db)
):
    """
    List all workout units for a user, optionally filtered by workout.
    """
    query = db.query(models.WorkoutUnit).filter(models.WorkoutUnit.user_name == user_name)
    if workout_id:
        query = query.filter(models.WorkoutUnit.workout_id == workout_id)
    return query.all()

@router.get("/workout_units/{id}", response_model=schemas.WorkoutUnit)
def read_workout_unit(id: int, db: Session = Depends(get_db)):
    """
    Get a single workout unit by its ID.
    """
    wu = db.query(models.WorkoutUnit).filter(models.WorkoutUnit.id == id).first()
    if not wu:
        raise HTTPException(status_code=404, detail="WorkoutUnit not found")
    return wu

@router.post("/workout_units", response_model=schemas.WorkoutUnit)
def create_workout_unit(wu: schemas.WorkoutUnitCreate, db: Session = Depends(get_db)):
    """
    Create a new workout unit.
    """
    db_wu = models.WorkoutUnit(**wu.dict())
    db.add(db_wu)
    db.commit()
    db.refresh(db_wu)
    return db_wu

@router.put("/workout_units/{id}", response_model=schemas.WorkoutUnit)
def update_workout_unit(id: int, wu: schemas.WorkoutUnitCreate, db: Session = Depends(get_db)):
    """
    Replace a workout unit by its ID.
    """
    db_wu = db.query(models.WorkoutUnit).filter(models.WorkoutUnit.id == id).first()
    if not db_wu:
        raise HTTPException(status_code=404, detail="WorkoutUnit not found")
    for key, value in wu.dict().items():
        setattr(db_wu, key, value)
    db.commit()
    db.refresh(db_wu)
    return db_wu

@router.delete("/workout_units/{id}", response_model=dict)
def delete_workout_unit(id: int, db: Session = Depends(get_db)):
    """
    Delete a workout unit by its ID.
    """
    db_wu = db.query(models.WorkoutUnit).filter(models.WorkoutUnit.id == id).first()
    if not db_wu:
        raise HTTPException(status_code=404, detail="WorkoutUnit not found")
    db.delete(db_wu)
    db.commit()
    return {"ok": True}