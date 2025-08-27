from sqlmodel import Column, Integer, String, BOOLEAN, SQLModel,Field
import pymysql as pym
from typing import Optional,Union
from pydantic import EmailStr
from datetime import date

#class Workout(SQLModel,table =True):
    


class User(SQLModel,table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: EmailStr = Field(sa_column=Column("email", String, unique=True, index=True))
    password: str = Field(sa_column=Column(String, nullable=False))
    


class UpdateWorkout(SQLModel):
    name: str
    exercise= Field(String)
    exercise_date: date=Field(String)
    sets: int=Field(Integer)
    reps: int=Field(Integer)