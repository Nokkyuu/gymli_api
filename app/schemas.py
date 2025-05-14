from pydantic import BaseModel, Field

class AnimalCreate(BaseModel):
    name: str = Field(..., example="Lion")
    sound: str = Field(..., example="Roar")

class Animal(AnimalCreate):
    id: int

    class Config:
        orm_mode = True