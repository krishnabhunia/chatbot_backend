# TODO : Basic Code V0:

# from pymongo import MongoClient

# # MongoDB connection setup
# client = MongoClient("mongodb://localhost:27017/")
# db = client.chatbot_db
# collection = db.conversations

# TODO : Enhanced Code V1 :
from pymongo import MongoClient
import os

# MongoDB connection setup
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)
db = client.chatbot_db
collection = db.conversations

# Ensure indexes for performance
db.conversations.create_index([("user_id", 1), ("conversation_id", 1)], unique=True)
