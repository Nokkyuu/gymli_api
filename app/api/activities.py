# Create app/api/activities.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app import models, schemas
from app.db import get_db

router = APIRouter()

def calculate_calories_burned(kcal_per_hour: float, duration_minutes: int) -> float:
    """Simple calorie calculation: (kcal/hour * minutes) / 60"""
    return round((kcal_per_hour * duration_minutes) / 60, 1)

@router.post("/users/{user_name}/initialize_activities")
def initialize_user_activities(user_name: str, db: Session = Depends(get_db)):
    """Initialize a new user with default activity types"""
    
    # Check if user already has activities
    existing = db.query(models.Activity).filter(models.Activity.user_name == user_name).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already has activities initialized")
    
    # Default activities with reasonable calorie estimates
    default_activities = [
        {"name": "Walking (casual)", "kcal_per_hour": 200},
        {"name": "Walking (brisk)", "kcal_per_hour": 300},
        {"name": "Running (light jog)", "kcal_per_hour": 400},
        {"name": "Running (moderate)", "kcal_per_hour": 600},
        {"name": "Running (fast)", "kcal_per_hour": 800},
        {"name": "Cycling (leisurely)", "kcal_per_hour": 300},
        {"name": "Cycling (moderate)", "kcal_per_hour": 500},
        {"name": "Swimming", "kcal_per_hour": 400},
        {"name": "Rowing machine", "kcal_per_hour": 450},
        {"name": "Elliptical", "kcal_per_hour": 350},
        {"name": "Stair climbing", "kcal_per_hour": 500},
        {"name": "Basketball", "kcal_per_hour": 450},
        {"name": "Soccer", "kcal_per_hour": 500},
        {"name": "Tennis", "kcal_per_hour": 400},
        {"name": "Yoga", "kcal_per_hour": 150},
        {"name": "Hiking", "kcal_per_hour": 350},
    ]
    
    for activity_data in default_activities:
        activity = models.Activity(user_name=user_name, **activity_data)
        db.add(activity)
    
    db.commit()
    return {"message": f"Initialized {len(default_activities)} activities for {user_name}"}

@router.get("/activities", response_model=List[schemas.Activity])
def get_user_activities(
    user_name: str = Query(..., description="Username to get activities for"),
    db: Session = Depends(get_db)
):
    """Get all activities for a specific user"""
    activities = db.query(models.Activity).filter(models.Activity.user_name == user_name).all()
    return activities

@router.post("/activities", response_model=schemas.Activity)
def create_activity(activity: schemas.ActivityCreate, db: Session = Depends(get_db)):
    """Create a new custom activity for user"""
    db_activity = models.Activity(**activity.dict())
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity

@router.put("/activities/{activity_id}", response_model=schemas.Activity)
def update_activity(
    activity_id: int, 
    activity_update: schemas.ActivityBase,
    user_name: str = Query(..., description="Username for authorization"),
    db: Session = Depends(get_db)
):
    """Update a user's activity"""
    activity = db.query(models.Activity).filter(
        models.Activity.id == activity_id,
        models.Activity.user_name == user_name
    ).first()
    
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    activity.name = activity_update.name # type: ignore
    activity.kcal_per_hour = activity_update.kcal_per_hour  # type: ignore # ADD THIS LINE
    
    db.commit()
    db.refresh(activity)
    return activity

@router.delete("/activities/{activity_id}")
def delete_activity(
    activity_id: int, 
    user_name: str = Query(..., description="Username for authorization"), 
    db: Session = Depends(get_db)
):
    """Delete a user's activity"""
    activity = db.query(models.Activity).filter(
        models.Activity.id == activity_id,
        models.Activity.user_name == user_name
    ).first()
    
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    db.delete(activity)
    db.commit()
    return {"message": "Activity deleted"}

@router.get("/activity_logs", response_model=List[schemas.ActivityLog])
def get_activity_logs(
    user_name: str = Query(..., description="Username to get logs for"),
    activity_name: Optional[str] = Query(None, description="Filter by specific activity name"),
    start_date: Optional[datetime] = Query(None, description="Filter from this date"),
    end_date: Optional[datetime] = Query(None, description="Filter until this date"),
    db: Session = Depends(get_db)
):
    """Get activity logs with optional filtering"""
    query = db.query(models.ActivityLog).filter(models.ActivityLog.user_name == user_name)
    
    if activity_name:
        query = query.filter(models.ActivityLog.activity_name == activity_name)
    if start_date:
        query = query.filter(models.ActivityLog.date >= start_date)
    if end_date:
        query = query.filter(models.ActivityLog.date <= end_date)
        
    return query.order_by(models.ActivityLog.date.desc()).all()

@router.post("/activity_logs", response_model=schemas.ActivityLog)
def create_activity_log(log_data: schemas.ActivityLogCreate, db: Session = Depends(get_db)):
    """Log a new activity session with automatic calorie calculation"""
    
    # Get the activity to access kcal_per_hour by name
    activity = db.query(models.Activity).filter(
        models.Activity.name == log_data.activity_name,
        models.Activity.user_name == log_data.user_name
    ).first()
    
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    # Calculate calories
    calories_burned = calculate_calories_burned(
        activity.kcal_per_hour, # type: ignore
        log_data.duration_minutes
    )
    
    # Create log entry
    log_dict = log_data.dict()
    log_dict['calories_burned'] = calories_burned
    
    db_log = models.ActivityLog(**log_dict)
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

@router.get("/activity_logs/stats")
def get_activity_stats(
    user_name: str = Query(..., description="Username to get stats for"),
    start_date: Optional[datetime] = Query(None, description="Stats from this date"),
    end_date: Optional[datetime] = Query(None, description="Stats until this date"),
    db: Session = Depends(get_db)
):
    """Get activity statistics for a user"""
    query = db.query(models.ActivityLog).filter(models.ActivityLog.user_name == user_name)
    
    if start_date:
        query = query.filter(models.ActivityLog.date >= start_date)
    if end_date:
        query = query.filter(models.ActivityLog.date <= end_date)
    
    logs = query.all()
    
    if not logs:
        return {
            "total_sessions": 0,
            "total_duration_minutes": 0,
            "total_calories_burned": 0,
            "average_session_duration": 0,
            "average_calories_per_session": 0
        }
    
    total_duration = sum(log.duration_minutes for log in logs)
    total_calories = sum(log.calories_burned for log in logs)
    session_count = len(logs)
    
    return {
        "total_sessions": session_count,
        "total_duration_minutes": total_duration,
        "total_calories_burned": round(total_calories, 1), # type: ignore
        "average_session_duration": round(total_duration / session_count, 1), # type: ignore
        "average_calories_per_session": round(total_calories / session_count, 1) # type: ignore
    }

@router.delete("/activity_logs/{log_id}")
def delete_activity_log(
    log_id: int,
    user_name: str = Query(..., description="Username for authorization"),
    db: Session = Depends(get_db)
):
    """Delete a user's activity log entry"""
    log = db.query(models.ActivityLog).filter(
        models.ActivityLog.id == log_id,
        models.ActivityLog.user_name == user_name
    ).first()
    if not log:
        raise HTTPException(status_code=404, detail="Activity log not found")
    db.delete(log)
    db.commit()
    return {"message": "Activity log deleted"}