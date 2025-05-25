from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.db import get_db

router = APIRouter()

# =========================
# Workout Endpoints
# =========================

@router.get("/workouts", response_model=List[schemas.Workout])
def read_workouts(
    user_name: str = Query(..., description="Username to filter workouts by"),
    db: Session = Depends(get_db)
):
    """
    List all workouts for a user.
    """
    return db.query(models.Workout).filter(models.Workout.user_name == user_name).all()

@router.get("/workouts/{id}", response_model=schemas.Workout)
def read_workout(id: int, db: Session = Depends(get_db)):
    """
    Get a single workout by its ID.
    """
    workout = db.query(models.Workout).filter(models.Workout.id == id).first()
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    return workout

@router.post("/workouts", response_model=schemas.Workout)
def create_workout(workout: schemas.WorkoutCreate, db: Session = Depends(get_db)):
    """
    Create a new workout.
    """
    db_workout = models.Workout(**workout.dict())
    db.add(db_workout)
    db.commit()
    db.refresh(db_workout)
    return db_workout

@router.put("/workouts/{id}", response_model=schemas.Workout)
def update_workout(id: int, workout: schemas.WorkoutCreate, db: Session = Depends(get_db)):
    """
    Replace a workout by its ID.
    """
    db_workout = db.query(models.Workout).filter(models.Workout.id == id).first()
    if not db_workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    for key, value in workout.dict().items():
        setattr(db_workout, key, value)
    db.commit()
    db.refresh(db_workout)
    return db_workout

@router.delete("/workouts/{id}", response_model=dict)
def delete_workout(id: int, db: Session = Depends(get_db)):
    """
    Delete a workout by its ID.
    """
    db_workout = db.query(models.Workout).filter(models.Workout.id == id).first()
    if not db_workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    db.delete(db_workout)
    db.commit()
    return {"ok": True}