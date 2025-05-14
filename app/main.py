from fastapi import FastAPI
from app.api import animals

app = FastAPI(title="Animal API")

app.include_router(animals.router)