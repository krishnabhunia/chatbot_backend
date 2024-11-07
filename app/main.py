# TODO : Basic Code V0:

# from fastapi import FastAPI
# from app.routes import conversation

# app = FastAPI()

# # Include conversation routes
# app.include_router(conversation.router)

# # Run the app with:
# # uvicorn app.main:app --reload

# TODO : Enhanced Code V1 :
from fastapi import FastAPI
from app.routes import conversation
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Include conversation routes
app.include_router(conversation.router)

# Run the app with:
# uvicorn app.main:app --reload
