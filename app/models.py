# Currently, there are no additional models to define beyond what is in schemas.py
# You can define additional MongoDB models or utility functions here if needed

# Example of a utility function to generate unique IDs using ObjectId
from bson import ObjectId

def generate_id():
    return str(ObjectId())
