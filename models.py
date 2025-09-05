from sqlmodel import Column, Integer, String,SQLModel,Field, Date
from typing import Optional
from pydantic import EmailStr
from datetime import date


#class Workout(SQLModel,table =True):
    


class User(SQLModel,table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: EmailStr = Field(sa_column=Column(String(255), unique=True, index=True))
    password: str = Field(sa_column=Column(String(255), nullable=False))
    


class UpdateWorkout(SQLModel, table=True):
    
    exercise: str= Field(sa_column=Column(String(255), nullable=False,primary_key=True))
    exercise_date: date=Field(default_factory=date.today(),sa_column=Column(Date,nullable=False))
    sets: int=Field(sa_column=Column(Integer, nullable=False))