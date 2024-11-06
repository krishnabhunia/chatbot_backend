from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from bson import ObjectId

class Message(BaseModel):
    message_id: str = Field(default_factory=lambda: str(ObjectId()))
    sender: str
    content: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    file_url: Optional[str] = None
    image_url: Optional[str] = None

class ConversationHistory(BaseModel):
    

class Conversation(BaseModel):
    user_id: str
    conversation_id: str = Field(default_factory=lambda: str(ObjectId()))
    messages: List[Message] = []
