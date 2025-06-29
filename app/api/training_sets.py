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

@router.post("/training_sets/bulk", response_model=List[schemas.TrainingSet])
def create_training_sets_bulk(
    training_sets: List[schemas.TrainingSetCreate], 
    db: Session = Depends(get_db)
):
    """
    Create multiple training sets in a single batch operation.
    This endpoint is optimized for bulk imports and significantly reduces
    the number of HTTP requests compared to creating sets individually.
    
    Args:
        training_sets: List of training set data to create
        
    Returns:
        List of created training sets with their assigned IDs
        
    Raises:
        HTTPException: If there are validation errors or database issues
    """
    if not training_sets:
        raise HTTPException(status_code=400, detail="Training sets list cannot be empty")
    
    if len(training_sets) > 1000:  # Reasonable limit to prevent abuse
        raise HTTPException(status_code=400, detail="Cannot create more than 1000 training sets in a single request")
    
    created_sets = []
    
    try:
        # Create all training set objects
        for ts_data in training_sets:
            db_ts = models.TrainingSet(**ts_data.dict())
            db.add(db_ts)
            created_sets.append(db_ts)
        
        # Commit all at once for better performance
        db.commit()
        
        # Refresh all objects to get their IDs
        for db_ts in created_sets:
            db.refresh(db_ts)
        
        return created_sets
        
    except Exception as e:
        # Rollback transaction on error
        db.rollback()
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to create training sets in bulk: {str(e)}"
        )

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

@router.delete("/training_sets/bulk_clear", response_model=dict)
def clear_training_sets(user_name: str = Query(...), db: Session = Depends(get_db)):
    """
    Clear all training sets for a user using efficient bulk delete.
    """
    # Count first for the response message
    count = db.query(models.TrainingSet).filter(
        models.TrainingSet.user_name == user_name
    ).count()
    
    # OPTIMIZED: Single bulk DELETE operation
    db.query(models.TrainingSet).filter(
        models.TrainingSet.user_name == user_name
    ).delete()
    
    db.commit()
    return {"message": f"Cleared {count} training sets"}

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