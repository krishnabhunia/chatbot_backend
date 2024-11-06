# Define Pydantic models for chat-related data

from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class ChatMessage(BaseModel):
    message: str
    sender: str

class ChatSession(BaseModel):
    user_id: str

class ChatSessionInDB(ChatSession):
    start_time: datetime
    end_time: Optional[datetime] = None
    messages: List[ChatMessage] = [{"timestamp": datetime.utcnow(), "message": "Hello! Its chatbot. How Can I help you", "sender": "bot"}]
