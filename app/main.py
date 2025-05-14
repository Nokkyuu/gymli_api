from fastapi import FastAPI
from api import animals

app = FastAPI(title="Animal API")

app.include_router(animals.router)