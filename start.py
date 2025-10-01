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
            return result_res
    except Exception as e:
        return {"error": str(e)}
        


            

@app.post("/post_workouts")
def create_workout(workout: UpdateWorkout):
    try:


        with Session(engine) as session:
            workout=UpdateWorkout(exercise=workout.exercise, sets=workout.sets)
            session.add(workout)
            session.commit()
            return {"message": "Workout added successfully"}
    except Exception as e:
        return {"error": str(e)}
            