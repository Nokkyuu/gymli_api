from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class AnimalCreate(BaseModel):
    name: str = Field(..., examples=["Lion"])
    sound: str = Field(..., examples=["Roar"])

class Animal(AnimalCreate):
    id: int

    class Config:
        orm_mode = True

# =========================
# Exercise Schemas
# =========================

class ExerciseBase(BaseModel):
    user_name: str
    name: str
    type: int
    default_rep_base: int
    default_rep_max: int
    default_increment: float
    pectoralis_major: float = Field(0.0, ge=0.0, le=1.0)
    trapezius: float = Field(0.0, ge=0.0, le=1.0)
    biceps: float = Field(0.0, ge=0.0, le=1.0)
    abdominals: float = Field(0.0, ge=0.0, le=1.0)
    front_delts: float = Field(0.0, ge=0.0, le=1.0)
    deltoids: float = Field(0.0, ge=0.0, le=1.0)
    back_delts: float = Field(0.0, ge=0.0, le=1.0)
    latissimus_dorsi: float = Field(0.0, ge=0.0, le=1.0)
    triceps: float = Field(0.0, ge=0.0, le=1.0)
    gluteus_maximus: float = Field(0.0, ge=0.0, le=1.0)
    hamstrings: float = Field(0.0, ge=0.0, le=1.0)
    quadriceps: float = Field(0.0, ge=0.0, le=1.0)
    forearms: float = Field(0.0, ge=0.0, le=1.0)  # ✅ ADD THIS LINE
    calves: float = Field(0.0, ge=0.0, le=1.0)

class ExerciseCreate(ExerciseBase):
    pass

class Exercise(ExerciseBase):
    id: int

    class Config:
        orm_mode = True

# =========================
# TrainingSet Schemas
# =========================

class TrainingSetBase(BaseModel):
    user_name: str
    exercise_id: int
    date: datetime
    weight: float
    repetitions: int
    set_type: int
    base_reps: int
    max_reps: int
    increment: float
    machine_name: Optional[str] = None

class TrainingSetCreate(TrainingSetBase):
    pass

class TrainingSet(TrainingSetBase):
    id: int

    class Config:
        orm_mode = True

# =========================
# Workout Schemas
# =========================

class WorkoutBase(BaseModel):
    user_name: str
    name: str

class WorkoutCreate(WorkoutBase):
    pass

class Workout(WorkoutBase):
    id: int

    class Config:
        orm_mode = True

# =========================
# WorkoutUnit Schemas
# =========================

class WorkoutUnitBase(BaseModel):
    user_name: str
    exercise_id: int
    warmups: int
    worksets: int
    type: int
    workout_id: int

class WorkoutUnitCreate(WorkoutUnitBase):
    pass

class WorkoutUnit(WorkoutUnitBase):
    id: int

    class Config:
        orm_mode = True