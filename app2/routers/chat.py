# Define API endpoints related to chat operations

from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from ..models.chat import ChatSession, ChatMessage
from ..services.chat_service import ChatService
from bson import ObjectId
from datetime import datetime

router = APIRouter()

# Instantiate the chat service
chat_service = ChatService()

@router.post("/start_session", response_model=dict)
async def start_session(session: ChatSession):
    # Endpoint to start a new chat session
    chat_session = await chat_service.start_session(session)
    return {"session_id": str(chat_session["_id"])}

@router.post("/send_message/{session_id}", response_model=dict)
async def send_message(session_id: str, message: ChatMessage):
    # Endpoint to send a message in an existing chat session
    updated_session = await chat_service.send_message(session_id, message)
    if not updated_session:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"status": "Message added"}

@router.get("/get_history/{user_id}", response_model=dict)
async def get_history(user_id: str):
    # Endpoint to retrieve chat history for a user
    sessions = await chat_service.get_history(user_id)
    return {"sessions": sessions}

@router.post("/upload_file/{session_id}", response_model=dict)
async def upload_file(session_id: str, file: UploadFile = File(...)):
    # Endpoint to upload a file to a chat session
    filename, content_type = await chat_service.upload_file(session_id, file)
    return {"filename": filename, "content_type": content_type}
