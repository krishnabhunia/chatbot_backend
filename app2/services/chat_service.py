# Implement business logic for chat operations

from ..utils.database import get_database
from ..models.chat import ChatSession, ChatMessage
from bson import ObjectId
from datetime import datetime

class ChatService:
    def __init__(self):
        # Initialize database connection
        self.db = get_database()
        self.chat_collection = self.db["chat_sessions"]

    async def start_session(self, session: ChatSession):
        # Start a new chat session
        chat_session = {
            "user_id": session.user_id,
            "start_time": datetime.utcnow(),
            "end_time": None,
            "messages": [{"timestamp": datetime.utcnow(), "message": "Hello! Its chatbot. How Can I help you", "sender": "bot"}]
        }
        result = await self.chat_collection.insert_one(chat_session)
        return chat_session

    async def send_message(self, session_id: str, message: ChatMessage):
        # Send a message in an existing chat session
        new_message = {"timestamp": datetime.utcnow(), "message": message.message, "sender": message.sender}
        result = await self.chat_collection.update_one({"_id": ObjectId(session_id)}, {"$push": {"messages": new_message}})
        if result.modified_count == 0:
            return None
        return await self.chat_collection.find_one({"_id": ObjectId(session_id)})

    async def get_history(self, user_id: str):
        # Retrieve chat history for a user
        sessions = await self.chat_collection.find({"user_id": user_id}).to_list(length=100)
        return sessions

    async def upload_file(self, session_id: str, file: UploadFile):
        # Handle file upload in a chat session
        contents = await file.read()
        filename = file.filename
        content_type = file.content_type
        # Save the file or process it as needed, this is just a stub.
        return filename, content_type
