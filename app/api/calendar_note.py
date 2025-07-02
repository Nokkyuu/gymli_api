from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from app import models, schemas
from app.db import get_db

router = APIRouter()

@router.get("/calendar_notes", response_model=List[schemas.CalendarNote])
def get_calendar_notes(user_name: str = Query(...), db: Session = Depends(get_db)):
    return db.query(models.CalendarNote).filter(models.CalendarNote.user_name == user_name).all()

@router.post("/calendar_notes", response_model=schemas.CalendarNote)
def create_calendar_note(note: schemas.CalendarNoteCreate, db: Session = Depends(get_db)):
    db_note = models.CalendarNote(**note.dict())
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note  

@router.put("/calendar_notes/{note_id}", response_model=schemas.CalendarNote)
def update_calendar_note(note_id: int, note: schemas.CalendarNoteCreate, db: Session = Depends(get_db)):
    """Update an existing calendar note"""
    db_note = db.query(models.CalendarNote).filter(models.CalendarNote.id == note_id).first()
    if not db_note:
        raise HTTPException(status_code=404, detail="Calendar note not found")
    
    # Update the note fields
    for field, value in note.dict().items():
        setattr(db_note, field, value)
    
    db.commit()
    db.refresh(db_note)
    return db_note

@router.delete("/calendar_notes/{note_id}")
def delete_calendar_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(models.CalendarNote).filter(models.CalendarNote.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Calendar note not found")
    db.delete(note)
    db.commit()
    return {"message": "Calendar note deleted"}