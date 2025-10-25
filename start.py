from fastapi import FastAPI,Request,HTTPException, status, Depends
from pydantic import EmailStr
from sqlmodel import select,Session
from datetime import timedelta
from jose import JWTError, jwt
from models import UpdateWorkout, User
from passlib.context import CryptContext
from database import engine
import bcrypt
from datetime import datetime,timezone
from typing import Optional
from config import sec_key, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES


def getssession():
    with Session(engine) as session:
        yield session

pwd_context = CryptContext(schemes=[bcrypt], deprecated="auto")

def get_passhash(password: str):
    return pwd_context.hash(password)
def verifypass(plain_pass:str, hashed_pass: str):
    return pwd_context.verify(plain_pass, hashed_pass)

def create_access_token(email: str):
    expiry_time=datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload={"sub":email, "exp":expiry_time}
    return jwt.encode(payload,sec_key,algorithm=ALGORITHM)

app = FastAPI()


def get_current_user(authorization: Optional[str]=(None), session: Session=Depends(getssession)):

    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header missing")
    token=authorization.split()
    try:
        payload=jwt.decode(token,sec_key,algorithms=[ALGORITHM])
        email=payload.get("sub")
        if not email:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="invalid token")
        statement=select(User).where(User.email==email)
        result=session.exec(statement).first()
        if not result:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="User not found")
        return result
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")
    





@app.get("/")
def read_root():
    return {"Hello": "World"}



@app.post("/Sign in")
def Sign_in(email:EmailStr, password:str, session: Session=Depends(getssession)):
    try:
        
        statement = select(User).where(User.email==email)
        result = session.exec(statement).first()
        if result is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        if not bcrypt.checkpw(password.encode('utf-8'),result.password.encode('utf-8')):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password")
            
        token=create_access_token(email=result.email)
        return {"access token": token}
    except HTTPException:
        raise 
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error: {e}")


@app.post("/Sign_up")
def Sign_up(name:str,email:EmailStr,password:str,session: Session=Depends(getssession)):
    try:
        with Session(engine) as session:
            hashed_password=get_passhash(password)
            user=User(name=name,email=email,password=hashed_password)
            session.add(user)
            session.commit()
            return {"message": "User created succssfully"}
    except HTTPException:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")
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
            workout=UpdateWorkout(exercise=workout.exercise, sets=workout.sets,email=workout.email)
            session.add(workout)
            session.commit()
            return {"message": "Workout added successfully"}
    except Exception as e:
        return {"error": str(e)}
    
            