from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app import models, schemas
from app.db import get_db

router = APIRouter()

@router.get("/foods", response_model=List[schemas.FoodItem])
def get_user_foods(user_name: str = Query(...), db: Session = Depends(get_db)):
    return db.query(models.FoodItem).filter(models.FoodItem.user_name == user_name).all()

@router.post("/foods", response_model=schemas.FoodItem)
def create_food(food: schemas.FoodItemCreate, db: Session = Depends(get_db)):
    db_food = models.FoodItem(**food.dict())
    db.add(db_food)
    db.commit()
    db.refresh(db_food)
    return db_food

@router.delete("/foods/{food_id}")
def delete_food(food_id: int, user_name: str = Query(...), db: Session = Depends(get_db)):
    food = db.query(models.FoodItem).filter(models.FoodItem.id == food_id, models.FoodItem.user_name == user_name).first()
    if not food:
        raise HTTPException(status_code=404, detail="Food item not found")
    db.delete(food)
    db.commit()
    return {"message": "Food deleted"}

@router.get("/food_logs", response_model=List[schemas.FoodLog])
def get_food_logs(
    user_name: str = Query(...),
    food_name: Optional[str] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(models.FoodLog).filter(models.FoodLog.user_name == user_name)
    if food_name:
        query = query.filter(models.FoodLog.food_name == food_name)
    if start_date:
        query = query.filter(models.FoodLog.date >= start_date)
    if end_date:
        query = query.filter(models.FoodLog.date <= end_date)
    return query.order_by(models.FoodLog.date.desc()).all()

@router.post("/food_logs", response_model=schemas.FoodLog)
def create_food_log(log: schemas.FoodLogCreate, db: Session = Depends(get_db)):
    db_log = models.FoodLog(**log.dict())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

@router.delete("/food_logs/{log_id}")
def delete_food_log(log_id: int, user_name: str = Query(...), db: Session = Depends(get_db)):
    log = db.query(models.FoodLog).filter(models.FoodLog.id == log_id, models.FoodLog.user_name == user_name).first()
    if not log:
        raise HTTPException(status_code=404, detail="Food log not found")
    db.delete(log)
    db.commit()
    return {"message": "Food log deleted"}