from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Date, Boolean
from sqlalchemy.orm import relationship
from app.db import Base

class Animal(Base): ### for testing purposes
    """Animal table for testing purposes."""
    __tablename__ = "animals"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    sound = Column(String, nullable=False)

# The Exercise table stores user-defined exercises.
class Exercise(Base):
    __tablename__ = "exercises"  # Table name in PostgreSQL

    id = Column(Integer, primary_key=True, index=True) 
    user_name = Column(String, nullable=False, index=True)  # The name of the user this exercise belongs to, indexed for efficient queries
    name = Column(String, nullable=False)  # Name of the exercise (e.g., "Bench Press")
    type = Column(Integer, nullable=False)  # Integer indicating the type (e.g., Free, Machine, etc.)
    default_rep_base = Column(Integer, nullable=False)  # Default minimum reps
    default_rep_max = Column(Integer, nullable=False)  # Default maximum reps
    default_increment = Column(Float, nullable=False)  # Default weight increment

    # Each muscle group gets its own column, representing intensity (float between 0 and 1)
    pectoralis_major = Column(Float, default=0.0)
    trapezius = Column(Float, default=0.0)
    biceps = Column(Float, default=0.0)
    abdominals = Column(Float, default=0.0)
    front_delts = Column(Float, default=0.0)
    deltoids = Column(Float, default=0.0)
    back_delts = Column(Float, default=0.0)
    latissimus_dorsi = Column(Float, default=0.0)
    triceps = Column(Float, default=0.0)
    gluteus_maximus = Column(Float, default=0.0)
    hamstrings = Column(Float, default=0.0)
    quadriceps = Column(Float, default=0.0)
    calves = Column(Float, default=0.0)
    forearms = Column(Float, default=0.0)

    # Relationships to other tables
    training_sets = relationship("TrainingSet", back_populates="exercise")  # Links to all TrainingSet rows for this Exercise
    workout_units = relationship("WorkoutUnit", back_populates="exercise")  # Links to all WorkoutUnit rows for this Exercise

# The TrainingSet table tracks a single set performed by the user.
class TrainingSet(Base):
    __tablename__ = "training_sets"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, nullable=False, index=True)
    exercise_id = Column(Integer, ForeignKey("exercises.id"), nullable=False)
    date = Column(DateTime, nullable=False)
    weight = Column(Float, nullable=False)
    repetitions = Column(Integer, nullable=False)
    set_type = Column(Integer, nullable=False)
    phase = Column(String, nullable=True)           
    myoreps = Column(Boolean, nullable=True)        
    # Relationship to WorkoutUnit
    workout_units = relationship("WorkoutUnit", back_populates="training_set")

    # Relationship to Exercise
    exercise = relationship("Exercise", back_populates="training_sets")

# A WorkoutUnit is a component of a workout (represents one exercise within a workout, with set counts).
class WorkoutUnit(Base):
    __tablename__ = "workout_units"

    id = Column(Integer, primary_key=True, index=True)  # Unique ID
    user_name = Column(String, nullable=False, index=True)  # User-specific
    exercise_id = Column(Integer, ForeignKey("exercises.id"), nullable=False)  # Foreign key to Exercise
    warmups = Column(Integer, nullable=False)  # Number of warmup sets
    worksets = Column(Integer, nullable=False)  # Number of work sets
    type = Column(Integer, nullable=False)  # Type of unit (mirrors Exercise type? Or set type?)
    workout_id = Column(Integer, ForeignKey("workouts.id"), nullable=False)  # Foreign key to the Workout containing this unit

    # Relationships
    exercise = relationship("Exercise", back_populates="workout_units")  # Link to Exercise
    workout = relationship("Workout", back_populates="units")  # Link to parent Workout

# The Workout table represents a user-defined workout, which consists of multiple WorkoutUnits.
class Workout(Base):
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True, index=True)  # Unique ID
    user_name = Column(String, nullable=False, index=True)  # User-specific
    name = Column(String, nullable=False)  # Name of the workout (e.g., "Push Day")
    units = relationship("WorkoutUnit", back_populates="workout", cascade="all, delete-orphan")
    # Relationship: deleting a Workout also deletes all its WorkoutUnits

# Add these to your app/models.py file

class Activity(Base):
    """Activity table for tracking different types of physical activities."""
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, nullable=False, index=True)
    name = Column(String, nullable=False)  # e.g., "Running", "Walking", "Rowing"
    kcal_per_hour = Column(Float, nullable=False)  # User-defined calories per hour

class ActivityLog(Base):
    """Activity log table for tracking user's activity sessions."""
    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, nullable=False, index=True)
    activity_name = Column(String, nullable=False)  # Store activity name directly
    date = Column(DateTime, nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    calories_burned = Column(Float, nullable=False)  # Calculated from duration and kcal_per_hour
    notes = Column(String, nullable=True)


class FoodItem(Base):
    __tablename__ = "food_items"
    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, nullable=False, index=True)  # user-specific
    name = Column(String, nullable=False)
    kcal_per_100g = Column(Float, nullable=False)
    protein_per_100g = Column(Float, nullable=False)
    carbs_per_100g = Column(Float, nullable=False)
    fat_per_100g = Column(Float, nullable=False)
    notes = Column(String, nullable=True)

class FoodLog(Base):
    __tablename__ = "food_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, nullable=False, index=True)
    food_name = Column(String, nullable=False)  # store name for log consistency
    date = Column(DateTime, nullable=False)
    grams = Column(Float, nullable=False)
    kcal_per_100g = Column(Float, nullable=False)
    protein_per_100g = Column(Float, nullable=False)
    carbs_per_100g = Column(Float, nullable=False)
    fat_per_100g = Column(Float, nullable=False)

class CalendarNote(Base):
    __tablename__ = "calendar_notes"
    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, nullable=False, index=True)
    date = Column(Date, nullable=False)
    note = Column(String, nullable=False)

class CalendarWorkout(Base):
    __tablename__ = "calendar_workouts"
    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, nullable=False, index=True)
    date = Column(Date, nullable=False)
    workout = Column(String, nullable=False)

class Period(Base):
    __tablename__ = "periods"
    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, nullable=False, index=True)
    type = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)