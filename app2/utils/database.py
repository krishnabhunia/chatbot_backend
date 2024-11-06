# Utility functions for database connection

from motor.motor_asyncio import AsyncIOMotorClient
from ..config import settings

def get_database():
    # Get the database connection
    client = AsyncIOMotorClient(settings.mongo_connection_string)
    return client[settings.database_name]
