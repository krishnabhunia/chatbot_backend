from pydantic import BaseModel,HttpUrl
from typing import List, Optional
from io import BytesIO

class MessageHistory(BaseModel):
    user: str
    chatbot_response: str
    download_link: Optional[str] = None  # Optional URL link given by chatbot for downloading    
    # file: Optional[bytes] = None  # Optional file, using bytes to represent the uploaded file, this is given by User  : TBD
    

class Conversation(BaseModel):
    user_id: str
    conversation_id: str
    message_history: List[MessageHistory]
