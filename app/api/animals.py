from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import SessionLocal
from models import Animal as DBAnimal
from schemas import AnimalCreate, Animal

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/animals", response_model=Animal)
def create_animal(animal: AnimalCreate, db: Session = Depends(get_db)):
    db_animal = DBAnimal(name=animal.name, sound=animal.sound)
    db.add(db_animal)
    db.commit()
    db.refresh(db_animal)
    return db_animal