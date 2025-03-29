from pymongo import MongoClient
from dotenv import load_dotenv
import os
from bson.objectid import ObjectId
import uuid

# Load environment variables
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client["VibeEase"]
users_collection = db["users"]
conversation_collection = db["conversation"]

# 1. Create a new conversation between two users
def create_conversation(user1_id, user2_id):
    user1 = users_collection.find_one({"_id": ObjectId(user1_id)})
    user2 = users_collection.find_one({"_id": ObjectId(user2_id)})

    if not user1 or not user2:
        raise ValueError("One or both users not found.")

    conversation = {
        "users": [user1, user2],
        "dialogue": []
    }

    result = conversation_collection.insert_one(conversation)
    print(f"Conversation created with ID: {result.inserted_id}")
    return result.inserted_id

# 2. Add a message to the conversation
def add_dialogue(conversation_id: str, new_message: str):
    result = conversation_collection.update_one(
        {"_id": conversation_id},
        {"$push": {"dialogue": new_message}}
    )
    if result.modified_count == 0:
        print("No conversation found or message not added.")
    else:
        print("Message added successfully.")

# 3. Remove a conversation
def remove_conversation(conversation_id: str):
    result = conversation_collection.delete_one({"_id": ObjectId(conversation_id)})
    if result.deleted_count == 0:
        print("Conversation not found.")
    else:
        print("Conversation deleted successfully.")

