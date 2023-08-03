from dotenv import load_dotenv
from app.db import Database

def validate_db():
    
    load_dotenv()

    db = Database()

    if db.mongo_collection is not None:
        print("Mongo service is connected")

    if db.db is not None:
        print("MySQL is connected")