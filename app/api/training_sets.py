from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from app import models, schemas
from app.db import get_db
from typing import Dict

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

@router.get("/training_sets/last_dates", response_model=Dict[str, str])
def read_last_training_dates_per_exercise(
    user_name: str = Query(..., description="Username to get last training dates for"), 
    db: Session = Depends(get_db)
):
    """
    Get the last training date for each exercise for a specific user.
    Returns a dictionary mapping exercise names to their last training dates.
    This endpoint is optimized for performance compared to fetching all training sets.
    """
    
    # Optimized query using JOIN and GROUP BY to get last date per exercise
    query = (
        db.query(
            models.Exercise.name.label('exercise_name'),
            func.max(models.TrainingSet.date).label('last_training_date')
        )
        .join(models.Exercise, models.TrainingSet.exercise_id == models.Exercise.id)
        .filter(models.TrainingSet.user_name == user_name)
        .group_by(models.Exercise.name, models.Exercise.id)
    )
    
    results = query.all()
    
    # Convert results to dictionary format expected by the client
    last_dates = {}
    for row in results:
        # Convert datetime to ISO string format for JSON serialization
        if row.last_training_date:
            last_dates[row.exercise_name] = row.last_training_date.isoformat()
    
    return last_dates