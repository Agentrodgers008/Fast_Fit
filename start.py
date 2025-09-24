from fastapi import FastAPI,Request
from typing import Optional,Union
from pydantic import EmailStr
from sqlmodel import select,Session
import json
from dotenv import load_dotenv
import os
import datetime
from models import UpdateWorkout
from database import engine
load_dotenv()
app = FastAPI()



@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/workouts")
def show_wkts(workoutname: Optional[str] = None):
    try:
        with Session(engine) as session:
            statement = select(UpdateWorkout).where(UpdateWorkout.exercise == workoutname)
            result_res = session.exec(statement).all()
        


            

@app.post("/workouts")
def create_workout():
    with open("data.json", "r") as file:
        data = json.load(file)
    data[workout.name] = workout.exercises
    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)
    return {"message": "Workout created successfully", "workout": workout}

@app.put("/update/{workoutname}")
def update_wkts():
    with open("data.json","r") as file:
        data=json.load(file)
        if workoutname in data:
            if data[workoutname] != None:
                data[workoutname] = workout.exercises
                with open("data.json", "w") as file:
                    json.dump(data, file, indent=4)
                
                return {"message": "Workout updated successfully", "workout": workout}