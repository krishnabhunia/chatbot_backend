from fastapi import FastAPI, HTTPException, UploadFile, File, Query
from typing import List
from app import crud
from app.schemas import Message

app = FastAPI()

@app.post("/conversations")
# def create_conversation(user_id: str):
#     conversation_id = crud.create_conversation(user_id)
#     return {"conversation_id": conversation_id}
def create_conversation(user_id: str = Query(...)):
    conversation_id = crud.create_conversation(user_id)
    return {"conversation_id": conversation_id}


@app.post("/conversations/{conversation_id}/messages")
def add_message(conversation_id: str, message: Message):
    if not crud.add_message(conversation_id, message):
        raise HTTPException(status_code=404, detail="Conversation not found")
    return {"status": "message added"}

@app.get("/users/{user_id}/conversations")
def get_conversations(user_id: str):
    return {"conversations": crud.get_conversations(user_id)}

@app.get("/conversations/{conversation_id}/messages")
def get_messages(conversation_id: str):
    messages = crud.get_messages(conversation_id)
    if messages is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return {"messages": messages}

@app.post("/conversations/{conversation_id}/upload")
async def upload_file(conversation_id: str, file: UploadFile = File(...)):
    file_url = f"http://example.com/{file.filename}"  # Replace with actual file storage logic
    message = Message(sender="user", file_url=file_url)
    if not crud.add_message(conversation_id, message):
        raise HTTPException(status_code=404, detail="Conversation not found")
    return {"status": "file uploaded", "file_url": file_url}

@app.post("/conversations/{conversation_id}/generate_image")
def generate_image(conversation_id: str):
    image_url = "http://example.com/generated_image.png"  # Replace with actual image generation logic
    message = Message(sender="bot", image_url=image_url)
    if not crud.add_message(conversation_id, message):
        raise HTTPException(status_code=404, detail="Conversation not found")
    return {"status": "image generated", "image_url": image_url}

@app.post("/conversations/{conversation_id}/generate_file")
def generate_file(conversation_id: str):
    file_url = "http://example.com/generated_file.xml"  # Replace with actual file generation logic
    message = Message(sender="bot", file_url=file_url)
    if not crud.add_message(conversation_id, message):
        raise HTTPException(status_code=404, detail="Conversation not found")
    return {"status": "file generated", "file_url": file_url}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
