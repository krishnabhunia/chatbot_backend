from pymongo import MongoClient

# MongoDB connection setup
client = MongoClient("mongodb://localhost:27017/")
# db = client.chatbot_db
db = client.db_kris_chatbot
collection = db.conversations