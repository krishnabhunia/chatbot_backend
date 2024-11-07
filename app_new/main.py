from fastapi import FastAPI
from app_new.chat_routes import router

app = FastAPI()

# Include routes
app.include_router(router)

# Run the app with:
# uvicorn app.main:app --reload
