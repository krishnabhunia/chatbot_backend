# Configuration settings for the application

from pydantic import BaseSettings

class Settings(BaseSettings):
    mongo_connection_string: str = "mongodb://localhost:27017"
    database_name: str = "chatbot_2"

    class Config:
        env_file = ".env"

settings = Settings()
