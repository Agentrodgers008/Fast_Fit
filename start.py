from fastapi import FastAPI
from pydantic import BaseModel
import json
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/workouts")
def read_workouts():
    with open("data.json", "r") as f:
        data=json.load(f)
        return data