from fastapi import APIRouter, HTTPException
from app.models import Chat, Message
from app.database import db
from datetime import datetime

router = APIRouter()  # Define the router instance here


# CREATE a new chat for a user
@router.post("/create_chat/{user_id}")
async def create_chat(user_id: str, chat: Chat):
    user = db.chats.find_one({"user_id": user_id})

    # If user doesn't exist, create a new user with the chat
    if not user:
        user_data = {
            "user_id": user_id,
            "chats": [chat.dict()]
        }
        db.chats.insert_one(user_data)
        return {"status": "Chat created for new user"}

    # Check if chat_id already exists for the user
    if any(existing_chat["chat_id"] == chat.chat_id for existing_chat in user["chats"]):
        raise HTTPException(status_code=400, detail="Chat ID already exists for this user")

    # Append the new chat to the existing user
    db.chats.update_one(
        {"user_id": user_id},
        {"$push": {"chats": chat.dict()}}
    )
    return {"status": "Chat added for existing user"}


# ADD a new message to an existing chat
@router.put("/add_message/{user_id}/{chat_id}")
async def add_message(user_id: str, chat_id: str, message: Message):
    # Check if the user exists
    user = db.chats.find_one({"user_id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if the chat exists for the user
    chat = next((c for c in user["chats"] if c["chat_id"] == chat_id), None)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found for this user")

    # Check for duplicate message_id within the chat
    if any(msg["message_id"] == message.message_id for msg in chat["messages"]):
        raise HTTPException(status_code=400, detail="Message ID already exists in this chat")

    # If everything is valid, add the message and update the chat's updated_at timestamp
    result = db.chats.update_one(
        {"user_id": user_id, "chats.chat_id": chat_id},
        {
            "$push": {"chats.$.messages": message.dict()},
            "$set": {"chats.$.updated_at": datetime.now()}
        }
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Failed to update chat with the new message")

    return {"status": "Message added to chat"}


# GET all chats for a user
@router.get("/get_chats/{user_id}")
async def get_chats(user_id: str):
    user = db.chats.find_one({"user_id": user_id}, {"_id": 0})
    if not user:
        raise HTTPException(status_code=404, detail="No chats found for this user")
    return user


# GET all messages in a specific chat
@router.get("/get_messages/{user_id}/{chat_id}")
async def get_messages(user_id: str, chat_id: str):
    user = db.chats.find_one(
        {"user_id": user_id, "chats.chat_id": chat_id},
        {"chats.$": 1, "_id": 0}
    )

    if not user or "chats" not in user or not user["chats"]:
        raise HTTPException(status_code=404, detail="Chat not found for this user")

    return user["chats"][0]["messages"]


# DELETE a chat
@router.delete("/delete_chat/{user_id}/{chat_id}")
async def delete_chat(user_id: str, chat_id: str):
    result = db.chats.update_one(
        {"user_id": user_id},
        {"$pull": {"chats": {"chat_id": chat_id}}}
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Chat not found for this user")
    return {"status": "Chat deleted"}


# DELETE a specific message in a chat
@router.delete("/delete_message/{user_id}/{chat_id}/{message_id}")
async def delete_message(user_id: str, chat_id: str, message_id: str):
    result = db.chats.update_one(
        {"user_id": user_id, "chats.chat_id": chat_id},
        {"$pull": {"chats.$.messages": {"message_id": message_id}}}
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Message not found in chat for this user")
    return {"status": "Message deleted"}


# UPDATE existing msg for a user and given chat id
@router.put("/update_message/{user_id}/{chat_id}/{message_id}")
async def update_message(user_id: str, chat_id: str, message_id: str, updated_message: Message):
    # Check if the user exists
    user = db.chats.find_one({"user_id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if the chat exists for the user
    chat = next((c for c in user["chats"] if c["chat_id"] == chat_id), None)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found for this user")

    # Check if the message exists in the chat based on URL `message_id`
    message = next((msg for msg in chat["messages"] if msg["message_id"] == message_id), None)
    if not message:
        raise HTTPException(status_code=404, detail="Message not found in chat for this user")

    # Check if the new `message_id` from JSON body already exists in the chat
    if any(msg["message_id"] == updated_message.message_id for msg in chat["messages"] if msg["message_id"] != message_id):
        raise HTTPException(status_code=400, detail="Message ID already exists in this chat")

    # Prepare the fields to update with the new message details
    update_fields = {
        "chats.$[chat].messages.$[msg].message_id": updated_message.message_id,
        "chats.$[chat].messages.$[msg].user_prompt": updated_message.user_prompt,
        "chats.$[chat].messages.$[msg].chatbot_answer": updated_message.chatbot_answer,
        "chats.$[chat].messages.$[msg].timestamp": updated_message.timestamp,
        "chats.$[chat].updated_at": datetime.now()  # Update the chat's last modified timestamp
    }

    # Perform the update using array filters to target specific chat and message
    result = db.chats.update_one(
        {"user_id": user_id},
        {"$set": update_fields},
        array_filters=[{"chat.chat_id": chat_id}, {"msg.message_id": message_id}]
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Failed to update message")

    return {"status": "Message updated successfully"}
