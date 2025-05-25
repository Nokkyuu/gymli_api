from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models import Animal as DBAnimal
from app.schemas import AnimalCreate, Animal
from app.db import get_db

router = APIRouter(
    prefix="/api/animals",
    tags=["animals"]
)


@router.post("/animals", response_model=Animal)
def create_animal(animal: AnimalCreate, db: Session = Depends(get_db)):
    db_animal = DBAnimal(name=animal.name, sound=animal.sound)
    db.add(db_animal)
    db.commit()
    db.refresh(db_animal)
    return db_animal

@router.get("/animals", response_model=list[Animal])
def get_animals(db: Session = Depends(get_db)):
    return db.query(DBAnimal).all()

@router.get("/animals/{animal_id}", response_model=Animal)
def get_animal(animal_id: int, db: Session = Depends(get_db)):
    animal = db.query(DBAnimal).filter(DBAnimal.id == animal_id).first()
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")
    return animal

@router.put("/animals/{animal_id}", response_model=Animal)
def update_animal(animal_id: int, updated: AnimalCreate, db: Session = Depends(get_db)):
    animal = db.query(DBAnimal).filter(DBAnimal.id == animal_id).first()
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")
    setattr(animal, "name", updated.name)
    setattr(animal, "sound", updated.sound)
    db.commit()
    db.refresh(animal)
    return animal

@router.delete("/animals/{animal_id}")
def delete_animal(animal_id: int, db: Session = Depends(get_db)):
    animal = db.query(DBAnimal).filter(DBAnimal.id == animal_id).first()
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")
    db.delete(animal)
    db.commit()
    return {"message": "Animal deleted"}