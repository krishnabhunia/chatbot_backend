from fastapi import FastAPI
from app.routes import conversation

app = FastAPI()

# Include conversation routes
app.include_router(conversation.router)

# Run the app with:
# uvicorn app.main:app --reload
