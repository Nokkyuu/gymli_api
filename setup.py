from app.db import Base, engine
from app.models import Animal, Exercise, TrainingSet, WorkoutUnit, Workout

#run only once to create table
Base.metadata.create_all(bind=engine)