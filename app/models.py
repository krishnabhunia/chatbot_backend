# Defines MongoDB models.

from pydantic import BaseModel
from typing import Optional, List, Dict

class Message(BaseModel):
    chat_id: str
    user_prompt: str
    chatbot_answer: str
    timestamp: str
    message_type: str = "text"
    metadata: Optional[Dict] = {}

class Chat(BaseModel):
    user_id: str
    created_at: str
    updated_at: str
    status: str
    metadata: Optional[Dict] = {}

class User(BaseModel):
    username: str
    email: str
    created_at: str
