# MongoDB connection setup.

import motor.motor_asyncio
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client.chatbot_ScaledDb  # The name of the MongoDB database

def get_database():
    return db
