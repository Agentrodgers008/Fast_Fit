from fastapi import FastAPI,Request
from typing import Optional,Union
from pydantic import EmailStr
from sqlmodel import SQLModel
import json
from pymysql import connect
import dotenv
import os
import datetime
load_dotenv()
conn=connect(
    host=os.getenv("host"),
    user=os.getenv("user"),
    password=os.getenv("password"),
    database=os.getenv("database")
    )

app = FastAPI()

class Workout(BaseModel):
    name: str
    exercises: Union[list[str],dict[str, list[str]]]


class User(BaseModel):
    mail: str
    passord: Union[str,int]



class UpdateWorkout(BaseModel):
    name: str
    exercises: Union[list[str],dict[str, list[str]]]

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

@app.put("/update/{workoutname}")
def update_wkts(workoutname: str, workout: UpdateWorkout):
    with open("data.json","r") as file:
        data=json.load(file)
        if workoutname in data:
            if data[workoutname] != None:
                data[workoutname] = workout.exercises
                with open("data.json", "w") as file:
                    json.dump(data, file, indent=4)
                
                return {"message": "Workout updated successfully", "workout": workout}