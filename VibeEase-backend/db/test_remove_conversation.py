from bson.objectid import ObjectId
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import uuid
from pprint import pprint
from conversation import remove_conversation

# Load env & connect
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["VibeEase"]
users_collection = db["users"]
conversation_collection = db["conversation"]

# Import your function
# from your_module import create_conversation, remove_conversation

# Step 1: Use two test users
user1_id = "67e8259487c915a2c5841751"
user2_id = "67e82599a7a20b37bda740fd"

# Step 2: Create a test conversation to delete
def test_create_temp_conversation(user1_id, user2_id):
    user1 = users_collection.find_one({"_id": ObjectId(user1_id)})
    user2 = users_collection.find_one({"_id": ObjectId(user2_id)})

    if not user1 or not user2:
        raise Exception("Test users not found.")

    conversation_id = str(uuid.uuid4())
    conversation = {
        "conversation_id": conversation_id,
        "users": [user1, user2],
        "dialogue": []
    }
    conversation_collection.insert_one(conversation)
    return conversation_id

# Step 3: Run test
try:
    temp_convo_id = test_create_temp_conversation(user1_id, user2_id)
    print(f"📦 Temporary conversation created with ID: {temp_convo_id}")

    remove_conversation(temp_convo_id)
    print("🗑️ Conversation removal attempted.")

    # Step 4: Verify deletion
    deleted = conversation_collection.find_one({"conversation_id": temp_convo_id})
    if deleted is None:
        print("✅ Test passed: Conversation successfully deleted.")
    else:
        print("❌ Test failed: Conversation still exists.")
        pprint(deleted)

except Exception as e:
    print(f"❌ Test failed with error: {e}")
