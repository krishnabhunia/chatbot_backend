# Pydantic models for request validation.

from pydantic import BaseModel
from typing import Optional, List

class MessageIn(BaseModel):
    user_prompt: str
    chatbot_answer: str
    timestamp: str

class ChatIn(BaseModel):
    user_id: str
    created_at: str
    updated_at: str
    status: str
    metadata: Optional[dict] = {}

class UserIn(BaseModel):
    username: str
    email: str
    created_at: str

class MessageOut(MessageIn):
    _id: str

class ChatOut(ChatIn):
    _id: str

class UserOut(UserIn):
    _id: str
