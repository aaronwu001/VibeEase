from bson.objectid import ObjectId
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from pprint import pprint
from conversation import add_dialogue

# Load environment variables and connect
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["VibeEase"]
conversation_collection = db["conversation"]

# Import the method to test
# from your_module import add_dialogue

# Step 1: Set a valid conversation_id (from a previously created conversation)
conversation_doc = conversation_collection.find_one()
if not conversation_doc:
    raise Exception("No conversation found in the database. Run the create_conversation test first.")

conversation_id = conversation_doc["conversation_id"]
new_message = "Hello, this is a test message!"

# Step 2: Run the function
try:
    add_dialogue(conversation_id, new_message)
    print("✅ Message added.")

    # Step 3: Check if the message was added
    updated_convo = conversation_collection.find_one({"conversation_id": conversation_id})
    if updated_convo and new_message in updated_convo.get("dialogue", []):
        print("🎯 Test passed: Message is in the dialogue list.")
    else:
        print("❌ Test failed: Message not found in dialogue.")
        pprint(updated_convo)
except Exception as e:
    print(f"❌ Test failed: {e}")
