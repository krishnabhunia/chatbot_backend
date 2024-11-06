from app.database import db
from app.schemas import Conversation, Message

def create_conversation(user_id: str) -> str:
    conversation = Conversation(user_id=user_id)
    db.conversations.insert_one(conversation.dict())
    return conversation.conversation_id

def add_message(conversation_id: str, message: Message) -> bool:
    result = db.conversations.update_one(
        {"conversation_id": conversation_id},
        {"$push": {"messages": message.dict()}}
    )
    return result.matched_count > 0

def get_conversations(user_id: str):
    conversations = list(db.conversations.find({"user_id": user_id}))
    for conv in conversations:
        conv["_id"] = str(conv["_id"])
    return conversations

def get_messages(conversation_id: str):
    conversation = db.conversations.find_one({"conversation_id": conversation_id})
    if not conversation:
        return None
    return conversation["messages"]
