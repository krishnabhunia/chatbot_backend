from pymongo import MongoClient

# MongoDB connection setup
client: MongoClient = MongoClient("mongodb://<WINDOWS_IP>:27017")
db = client.chatbot_db
collection = db.conversations
