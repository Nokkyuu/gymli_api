from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from app import models, schemas
from app.db import get_db

router = APIRouter()

@router.get("/calendar_workouts", response_model=List[schemas.CalendarWorkout])
def get_calendar_workouts(user_name: str = Query(...), db: Session = Depends(get_db)):
    return db.query(models.CalendarWorkout).filter(models.CalendarWorkout.user_name == user_name).all()

@router.post("/calendar_workouts", response_model=schemas.CalendarWorkout)
def create_calendar_workout(workout: schemas.CalendarWorkoutCreate, db: Session = Depends(get_db)):
    db_workout = models.CalendarWorkout(**workout.dict())
    db.add(db_workout)
    db.commit()
    db.refresh(db_workout)
    return db_workout  # This already returns the full object with ID

@router.delete("/calendar_workouts/{workout_id}")
def delete_calendar_workout(workout_id: int, db: Session = Depends(get_db)):
    workout = db.query(models.CalendarWorkout).filter(models.CalendarWorkout.id == workout_id).first()
    if not workout:
        raise HTTPException(status_code=404, detail="Calendar workout not found")
    db.delete(workout)
    db.commit()
    return {"message": "Calendar workout deleted"}