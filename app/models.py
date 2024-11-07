from pydantic import BaseModel
from typing import List
from datetime import datetime


class Message(BaseModel):
    message_id: str
    user_prompt: str
    chatbot_answer: str
    timestamp: datetime = datetime.now()


class Chat(BaseModel):
    chat_id: str
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    messages: List[Message]


class UserChats(BaseModel):
    user_id: str
    chats: List[Chat]
