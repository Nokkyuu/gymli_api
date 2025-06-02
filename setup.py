from app.db import Base, engine
from app.models import Animal, Exercise, TrainingSet, WorkoutUnit, Workout, Activity, ActivityLog

Base.metadata.create_all(bind=engine)
# This script initializes the database by creating all tables defined in the models.