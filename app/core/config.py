import os

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "leads_db")
EXTERNAL_API_URL = "https://dummyjson.com/users/1"
