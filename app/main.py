from fastapi import FastAPI, HTTPException, Depends, Header
from app.api import activities, animals, exercises, training_sets, workouts, workout_units, food, calendar_note, calendar_workout, period
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="Gymli API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://icy-ground-0e9ef4303.6.azurestaticapps.net", "https://gymli.brgmnn.de", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"], 
    allow_headers=["Content-Type", "Authorization", "Accept", "X-API-Key"],  # Add X-API-Key
)

API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY environment variable must be set")

async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key

# Include all routers
app.include_router(animals.router, dependencies=[Depends(verify_api_key)])
app.include_router(exercises.router, dependencies=[Depends(verify_api_key)])
app.include_router(training_sets.router, dependencies=[Depends(verify_api_key)])
app.include_router(workouts.router, dependencies=[Depends(verify_api_key)])
app.include_router(workout_units.router, dependencies=[Depends(verify_api_key)])
app.include_router(activities.router, dependencies=[Depends(verify_api_key)])
app.include_router(food.router, dependencies=[Depends(verify_api_key)])
app.include_router(calendar_note.router, dependencies=[Depends(verify_api_key)])
app.include_router(calendar_workout.router, dependencies=[Depends(verify_api_key)])
app.include_router(period.router, dependencies=[Depends(verify_api_key)])

@app.get("/")
def read_root():
    return {"status": "API is running"}

# Keep this endpoint public for health checks
@app.get("/health")
def health_check():
    return {"status": "healthy"}

