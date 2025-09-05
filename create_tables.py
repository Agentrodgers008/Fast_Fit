from database import create_tables
from models import User, UpdateWorkout

def main():
    create_tables()
    print("Tables have been added successfully")
if __name__ =="__main__":
    main()