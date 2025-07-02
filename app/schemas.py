from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from datetime import date

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
    # base_reps: int
    # max_reps: int
    # increment: float
    # machine_name: Optional[str] = None

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

# =========================
# Activity Schemas
# =========================
class ActivityBase(BaseModel):
    name: str = Field(..., max_length=100)
    kcal_per_hour: float = Field(..., gt=0)

class ActivityCreate(ActivityBase):
    user_name: str

class Activity(ActivityBase):
    id: int
    user_name: str

    class Config:
        orm_mode = True

# Activity Log Schemas
class ActivityLogBase(BaseModel):
    user_name: str
    activity_name: str 
    date: datetime
    duration_minutes: int = Field(..., gt=0)
    notes: Optional[str] = None

class ActivityLogCreate(ActivityLogBase):
    pass

class ActivityLog(ActivityLogBase):
    id: int
    calories_burned: float

    class Config:
        orm_mode = True

### Food Schemas
# ... (existing imports and schemas)

class FoodItemBase(BaseModel):
    name: str
    kcal_per_100g: float
    protein_per_100g: float
    carbs_per_100g: float
    fat_per_100g: float
    notes: Optional[str] = None

class FoodItemCreate(FoodItemBase):
    user_name: str

class FoodItem(FoodItemBase):
    id: int
    user_name: str
    class Config:
        orm_mode = True

class FoodLogBase(BaseModel):
    user_name: str
    food_name: str
    date: datetime
    grams: float
    kcal_per_100g: float
    protein_per_100g: float
    carbs_per_100g: float
    fat_per_100g: float

class FoodLogCreate(FoodLogBase):
    pass

class FoodLog(FoodLogBase):
    id: int
    class Config:
        orm_mode = True

### Calendar Schemas



class CalendarNoteBase(BaseModel):
    user_name: str
    date: date
    note: str

class CalendarNoteCreate(CalendarNoteBase):
    pass

class CalendarNote(CalendarNoteBase):
    id: int
    class Config:
        orm_mode = True

class CalendarWorkoutBase(BaseModel):
    user_name: str
    date: date
    workout: str

class CalendarWorkoutCreate(CalendarWorkoutBase):
    pass

class CalendarWorkout(CalendarWorkoutBase):
    id: int
    class Config:
        orm_mode = True

class PeriodBase(BaseModel):
    user_name: str
    type: str
    start_date: date
    end_date: date

class PeriodCreate(PeriodBase):
    pass

class Period(PeriodBase):
    id: int
    class Config:
        orm_mode = True