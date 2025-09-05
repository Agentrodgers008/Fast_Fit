# from sqlmodel import create_engine, Session, SQLModel

# SQLModel.metadata.create_all(engine)
# session_local=Session() #need to write proper code in sqlmodel specifications
from sqlmodel import SQLModel, create_engine
import cryptography

DATABASE_URL = "mysql+pymysql://root:Hkksangth8*@localhost:3306/fast_base"
engine = create_engine(DATABASE_URL)


def create_tables():
    SQLModel.metadata.create_all(engine)
