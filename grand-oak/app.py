from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from watchgod import run_process
import uvicorn

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Doctor(BaseModel):
    name: str
    category: str
    schedule: str
    fee: int

doctors = [
    Doctor(name="Thomas Collins", category="Surgery", schedule="9:00 AM - 11:00 AM", fee=7000),
    Doctor(name="Henry Parker", category="ENT", schedule="9:00 AM - 11:00 AM", fee=4500),
]

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/doctors", response_model=list[Doctor])
def get_doctors():
    return doctors

if __name__ == "__main__":
    run_process('.', lambda: uvicorn.run(app, host="0.0.0.0", port=8081))
