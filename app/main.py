# FastAPI application entry point.

from fastapi import FastAPI, HTTPException
from app.schemas import UserIn, ChatIn, MessageIn, UserOut, ChatOut, MessageOut
from app.crud import create_user, get_user, create_chat, get_chats_by_user, create_message, get_messages_by_chat
from typing import List

app = FastAPI()

@app.post("/users/", response_model=UserOut)
async def add_user(user: UserIn):
    return await create_user(user)

@app.get("/users/{user_id}", response_model=UserOut)
async def read_user(user_id: str):
    user = await get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/chats/", response_model=ChatOut)
async def add_chat(chat: ChatIn):
    return await create_chat(chat)

@app.get("/chats/{user_id}", response_model=List[ChatOut])
async def read_chats(user_id: str):
    return await get_chats_by_user(user_id)

@app.post("/messages/", response_model=MessageOut)
async def add_message(message: MessageIn):
    return await create_message(message)

@app.get("/messages/{chat_id}", response_model=List[MessageOut])
async def read_messages(chat_id: str):
    return await get_messages_by_chat(chat_id)
