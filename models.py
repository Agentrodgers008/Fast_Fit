from sqlmodel import Column, Integer, String, BOOLEAN, SQLModel,Field
from sqlalchemy import Column

class User(SQLModel,table=True):
    
    mail: str = Field(sa_column=Column(String, unique=True, index=True))
    password: str = Field(sa_column=Column(String(100)), min_length=8, description="Password must be at least 8 characters long")

class Workout(SQLModel,table=True):
    Set_number: int = Field(sa_column=Column(Integer, primary_key=True, autoincrement=True))