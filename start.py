from fastapi import FastAPI,Path,Query
from typing import Optional
from pydantic import BaseModel
import json
app = FastAPI()

class Workout(BaseModel):
    name: str
    exercises: list[str]

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/workouts")
def show_wkts(workoutname: Optional[str] = None):
    with open("data.json", "r") as data_show:
        show = json.load(data_show)
        if workoutname:
            if workoutname in show:
                return show[workoutname]
            else:
                return {"Error": "Workout not Found"}
        return show
@app.post("/workouts")
def create_workout(workout: Workout):
    with open("data.json", "r") as file:
        data = json.load(file)
    data[workout.name] = workout.exercises
    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)
    return {"message": "Workout created successfully", "workout": workout}