from pymongo import MongoClient

# load environment variable 
from dotenv import load_dotenv
import os
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

# Connect to MongoDB
client = MongoClient(MONGO_URI)

# Select the database and collection
db = client["VibeEase"]  
collection = db["users"]  

# Create a document (dictionary)
user1 = {
    "user_id": "A",
    "interest": ["music", "health", "home workouts"],
    "avoid": ["politics", "junk food"],
    "Amazon": ["yoga mat", "protein powder"],
    "Walmart": ["organic groceries", "fitness gear"],
    "Netflix": ["health documentaries", "calming nature shows"],
    "Spotify": ["ambient music", "yoga playlists"],
    "Pinterest": ["home gym ideas", "healthy meal prep"]
}

user2 = {
    "user_id": "B",
    "interest": ["music", "wellness", "meditation"],
    "avoid": ["violence", "toxic content"],
    "Amazon": ["meditation cushion", "herbal tea"],
    "Walmart": ["healthy snacks", "vitamins"],
    "Netflix": ["mindfulness series", "nature scenes"],
    "Spotify": ["lo-fi beats", "meditation tracks"],
    "Pinterest": ["calm space design", "clean eating tips"]
}

# Insert the document into the collection
result = collection.insert_one(user2)

# Print the auto-generated ObjectId
print("Document inserted with ID:", result.inserted_id)