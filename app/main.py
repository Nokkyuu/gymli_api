from fastapi import FastAPI
from app.api import activities, animals, exercises, training_sets, workouts, workout_units
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Gymli API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://icy-ground-0e9ef4303.6.azurestaticapps.net", "https://gymli.brgmnn.de", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routers
app.include_router(animals.router)
app.include_router(exercises.router)
app.include_router(training_sets.router)
app.include_router(workouts.router)
app.include_router(workout_units.router)
app.include_router(activities.router)

@app.get("/")
def read_root():
    return {"status": "API is running"}

