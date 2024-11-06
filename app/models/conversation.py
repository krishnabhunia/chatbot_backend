from pydantic import BaseModel
from typing import List

class MessageHistory(BaseModel):
    user: str
    chatbot_response: str

class Conversation(BaseModel):
    user_id: str
    conversation_id: str
    message_history: List[MessageHistory]
