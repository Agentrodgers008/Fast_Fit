from fastapi import FastAPI,Request,Depends,HTTPException
from pydantic import EmailStr
from sqlmodel import select,Session
import datetime
from models import UpdateWorkout, User
from database import engine
import bcrypt
app = FastAPI()



@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/Sign in")
def Sign_in(email:EmailStr, password:str):
    try:
        with Session(engine) as session:
            statement = select(User).where(User.email==email)
            result = session.exec(statement).first()
            if result is None:
                raise HTTPException(status_code=404, detail="User not found")
            if not bcrypt.checkpw(password.encode('utf-8'),result.password.encode('utf-8')):
                    raise HTTPException(status_code=400, detail="Incorrect password")
            
            return {"message": "Login successful"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")


@app.post("/Sign_up")
def Sign_up(name:str,email:EmailStr,password:str):
    password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    try:
        with Session(engine) as session:
            user=User(name=name,email=email,password=password)
            session.add(user)
            session.commit()
            return {"message": "User created succssfully"}
    except HTTPException as e:
        raise HTTPException(status_code=400, detail="Email already exists")
@app.get("/workouts")
def show_wkts():
    try:
        with Session(engine) as session:
            statement = select(UpdateWorkout)
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
    
            