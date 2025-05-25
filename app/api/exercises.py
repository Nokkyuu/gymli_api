from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.db import get_db

router = APIRouter(
    prefix="/api/exercises",
    tags=["exercises"]
)

# =========================
# Exercise Endpoints
# =========================

@router.get("/", response_model=List[schemas.Exercise])
def read_exercises(
    user_name: str = Query(..., description="Username to filter exercises by"),
    db: Session = Depends(get_db)
):
    """
    List all exercises for a user.
    """
    return db.query(models.Exercise).filter(models.Exercise.user_name == user_name).all()

@router.get("/{id}", response_model=schemas.Exercise)
def read_exercise(id: int, db: Session = Depends(get_db)):
    """
    Get a single exercise by its ID.
    """
    exercise = db.query(models.Exercise).filter(models.Exercise.id == id).first()
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return exercise

@router.post("/", response_model=schemas.Exercise)
def create_exercise(exercise: schemas.ExerciseCreate, db: Session = Depends(get_db)):
    """
    Create a new exercise.
    """
    db_exercise = models.Exercise(**exercise.dict())
    db.add(db_exercise)
    db.commit()
    db.refresh(db_exercise)
    return db_exercise

@router.put("/{id}", response_model=schemas.Exercise)
def update_exercise(id: int, exercise: schemas.ExerciseCreate, db: Session = Depends(get_db)):
    """
    Replace an exercise by its ID.
    """
    db_exercise = db.query(models.Exercise).filter(models.Exercise.id == id).first()
    if not db_exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    for key, value in exercise.dict().items():
        setattr(db_exercise, key, value)
    db.commit()
    db.refresh(db_exercise)
    return db_exercise

@router.delete("/{id}", response_model=dict)
def delete_exercise(id: int, db: Session = Depends(get_db)):
    """
    Delete an exercise by its ID.
    """
    db_exercise = db.query(models.Exercise).filter(models.Exercise.id == id).first()
    if not db_exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    db.delete(db_exercise)
    db.commit()
    return {"ok": True}