# TODO : Basic Code V0:

# from fastapi import APIRouter, HTTPException
# from app.models.conversation import Conversation, MessageHistory
# from app.database.mongodb import db

# router = APIRouter()

# # CREATE operation
# @router.post("/create_conversation")
# async def create_conversation(conversation: Conversation):
#     data = conversation.dict()
#     db.conversations.insert_one(data)
#     return {"status": "Conversation created successfully"}

# # DELETE operation
# @router.delete("/delete_conversation/{user_id}/{conversation_id}")
# async def delete_conversation(user_id: str, conversation_id: str):
#     result = db.conversations.delete_one({"user_id": user_id, "conversation_id": conversation_id})
#     if result.deleted_count == 0:
#         raise HTTPException(status_code=404, detail="Conversation not found")
#     return {"status": "Conversation deleted successfully"}

# # UPDATE operation
# @router.put("/update_conversation/{user_id}/{conversation_id}")
# async def update_conversation(user_id: str, conversation_id: str, message: MessageHistory):
#     result = db.conversations.update_one(
#         {"user_id": user_id, "conversation_id": conversation_id},
#         {"$push": {"message_history": message.dict()}}
#     )
#     if result.matched_count == 0:
#         raise HTTPException(status_code=404, detail="Conversation not found")
#     return {"status": "Conversation updated successfully"}

# # READ operation
# @router.get("/read_conversations/{user_id}")
# async def read_conversations(user_id: str):
#     conversations = list(db.conversations.find({"user_id": user_id}, {"_id": 0}))
#     if not conversations:
#         raise HTTPException(status_code=404, detail="No conversations found for this user")
#     return {"conversations": conversations}


# TODO : Enhanced Code V1 :
from fastapi import APIRouter, HTTPException
from app.models.conversation import Conversation, MessageHistory
from app.database.mongodb import db
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

# CREATE operation
@router.post("/create_conversation")
async def create_conversation(conversation: Conversation):
    existing_conversation = db.conversations.find_one({"user_id": conversation.user_id, "conversation_id": conversation.conversation_id})
    if existing_conversation:
        logger.warning(f"Duplicate conversation ID for user {conversation.user_id}")
        raise HTTPException(status_code=400, detail="Conversation ID already exists for this user")
    
    data = conversation.dict()
    db.conversations.insert_one(data)
    logger.info(f"Conversation created for user {conversation.user_id}")
    return {"status": "Conversation created successfully"}

# DELETE operation
@router.delete("/delete_conversation/{user_id}/{conversation_id}")
async def delete_conversation(user_id: str, conversation_id: str):
    result = db.conversations.delete_one({"user_id": user_id, "conversation_id": conversation_id})
    if result.deleted_count == 0:
        logger.error(f"Conversation not found for user {user_id} with conversation ID {conversation_id}")
        raise HTTPException(status_code=404, detail="Conversation not found")
    logger.info(f"Conversation deleted for user {user_id} with conversation ID {conversation_id}")
    return {"status": "Conversation deleted successfully"}

# UPDATE operation
@router.put("/update_conversation/{user_id}/{conversation_id}")
async def update_conversation(user_id: str, conversation_id: str, message: MessageHistory):
    result = db.conversations.update_one(
        {"user_id": user_id, "conversation_id": conversation_id},
        {"$push": {"message_history": message.dict()}}
    )
    if result.matched_count == 0:
        logger.error(f"Conversation not found for user {user_id} with conversation ID {conversation_id}")
        raise HTTPException(status_code=404, detail="Conversation not found")
    logger.info(f"Conversation updated for user {user_id} with conversation ID {conversation_id}")
    return {"status": "Conversation updated successfully"}

# READ operation
@router.get("/read_conversations/{user_id}")
async def read_conversations(user_id: str, skip: int = 0, limit: int = 10):
    conversations = list(db.conversations.find({"user_id": user_id}, {"_id": 0}).skip(skip).limit(limit))
    if not conversations:
        logger.error(f"No conversations found for user {user_id}")
        raise HTTPException(status_code=404, detail="No conversations found for this user")
    logger.info(f"Conversations retrieved for user {user_id}")
    return {"conversations": conversations}
