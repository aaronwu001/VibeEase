from conversation import create_conversation

# Test IDs (ObjectId from MongoDB)
user1_id = "67e8259487c915a2c5841751"
user2_id = "67e82599a7a20b37bda740fd"

# Call the create_conversation function with the two test users
try:
    conversation_id = create_conversation(user1_id, user2_id)
    print(f"✅ Test passed: Conversation created with ID {conversation_id}")
except Exception as e:
    print(f"❌ Test failed: {e}")
