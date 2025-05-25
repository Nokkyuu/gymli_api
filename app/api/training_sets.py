from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app import models, schemas
from app.db import get_db

router = APIRouter()

# =========================
# TrainingSet Endpoints
# =========================

@router.get("/training_sets", response_model=List[schemas.TrainingSet])
def read_training_sets(
    user_name: str = Query(..., description="Username to filter sets by"), 
    exercise_id: Optional[int] = Query(None, description="Exercise ID to filter sets by"), 
    db: Session = Depends(get_db)
):
    """
    List all training sets for a user, optionally filtered by exercise.
    """
    query = db.query(models.TrainingSet).filter(models.TrainingSet.user_name == user_name)
    if exercise_id:
        query = query.filter(models.TrainingSet.exercise_id == exercise_id)
    return query.all()

@router.get("/training_sets/{id}", response_model=schemas.TrainingSet)
def read_training_set(id: int, db: Session = Depends(get_db)):
    """
    Get a single training set by its ID.
    """
    ts = db.query(models.TrainingSet).filter(models.TrainingSet.id == id).first()
    if not ts:
        raise HTTPException(status_code=404, detail="TrainingSet not found")
    return ts

@router.post("/training_sets", response_model=schemas.TrainingSet)
def create_training_set(ts: schemas.TrainingSetCreate, db: Session = Depends(get_db)):
    """
    Create a new training set.
    """
    db_ts = models.TrainingSet(**ts.dict())
    db.add(db_ts)
    db.commit()
    db.refresh(db_ts)
    return db_ts

@router.put("/training_sets/{id}", response_model=schemas.TrainingSet)
def update_training_set(id: int, ts: schemas.TrainingSetCreate, db: Session = Depends(get_db)):
    """
    Replace a training set by its ID.
    """
    db_ts = db.query(models.TrainingSet).filter(models.TrainingSet.id == id).first()
    if not db_ts:
        raise HTTPException(status_code=404, detail="TrainingSet not found")
    for key, value in ts.dict().items():
        setattr(db_ts, key, value)
    db.commit()
    db.refresh(db_ts)
    return db_ts

@router.delete("/training_sets/{id}", response_model=dict)
def delete_training_set(id: int, db: Session = Depends(get_db)):
    """
    Delete a training set by its ID.
    """
    db_ts = db.query(models.TrainingSet).filter(models.TrainingSet.id == id).first()
    if not db_ts:
        raise HTTPException(status_code=404, detail="TrainingSet not found")
    db.delete(db_ts)
    db.commit()
    return {"ok": True}