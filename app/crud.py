# Defines the CRUD operations (e.g., create, read, update, delete).

from app.database import db
from app.models import User, Chat, Message
from app.schemas import UserIn, ChatIn, MessageIn
from bson import ObjectId

# Utility function to convert ObjectId to string
def str_object_id(obj):
    return str(obj["_id"])

# CRUD for Users
async def create_user(user: UserIn):
    user_doc = user.dict()
    result = await db.users.insert_one(user_doc)
    return {**user_doc, "_id": str(result.inserted_id)}

async def get_user(user_id: str):
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    if user:
        return {**user, "_id": str(user["_id"])}
    return None

# CRUD for Chats
async def create_chat(chat: ChatIn):
    chat_doc = chat.dict()
    result = await db.chats.insert_one(chat_doc)
    return {**chat_doc, "_id": str(result.inserted_id)}

async def get_chats_by_user(user_id: str):
    chats = []
    async for chat in db.chats.find({"user_id": user_id}):
        chats.append({**chat, "_id": str(chat["_id"])})
    return chats

# CRUD for Messages
async def create_message(message: MessageIn):
    message_doc = message.dict()
    result = await db.messages.insert_one(message_doc)
    return {**message_doc, "_id": str(result.inserted_id)}

async def get_messages_by_chat(chat_id: str):
    messages = []
    async for message in db.messages.find({"chat_id": chat_id}):
        messages.append({**message, "_id": str(message["_id"])})
    return messages
