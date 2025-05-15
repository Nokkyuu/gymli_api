from fastapi import FastAPI
from app.api import animals
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Animal API")

app.include_router(animals.router)

@app.get("/")
def read_root():
    return {"status": "API is running"}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://icy-ground-0e9ef4303.6.azurestaticapps.net/", "https://gymli.brgmnn.de/"],  # or specify: ["https://your-flutter-web-url"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)