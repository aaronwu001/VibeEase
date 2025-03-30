from google import genai

import os
import sys
sys.path.append(os.path.abspath("db"))
from conversation import create_conversation, add_dialogue, remove_conversation, get_conversation_by_id

# load environment variable 
from dotenv import load_dotenv
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def ask_gemini(query):
    client = genai.Client(api_key=GEMINI_API_KEY)
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=query,
    )
    return response


def generate_suggestion(conversation):
    # Organize the conversation history into a string
    dialogue = "\n".join(conversation.get('dialogue', ''))[-1800:]
    users = conversation.get('users') or {}

    # Construct the prompt for the Gemini model
    prompt = f"""

    You are an AI assistant that helps people communicate more smoothly by monitoring the emotional flow of a conversation.
    Your response must be within one sentence.
    
    You will be given:
    - Profiles: the two speakers' interests, topics they want to avoid, and recent topics based on activity history
    - A short conversation history between the two users

    Your tasks:
    1. Identify the current emotional state of both users (choose from: happy, neutral, sad, stressed, confused, frustrated).
    2. Determine if the current topic may cause discomfort or a negative reaction.
    3. Decide whether to continue the current topic or redirect the conversation.
    4. If redirection is needed, suggest a new topic based on shared interests and provide a starter sentence.
    5. Provide a short explanation of your reasoning.

    Profiles: 
    {str(users)}

    Here is the conversation history between A and B:
    {dialogue}
    
    Now, one user wants to continue the conversation. Based on the most recent part of the conversation, suggest a topic for them to discuss and explain how to introduce it.
    """

    # Use the Gemini model to generate a response (simulated here)
    topic_suggestion = ask_gemini(prompt).text
    
    return topic_suggestion


def update_conversation(conversation_id, new_message):

    if not conversation_id or not new_message:
        return {"error": "conversation_id and new_dialogue (text) are required"}

    try:
        # Step 1: Update conversation in MongoDB
        add_dialogue(conversation_id, new_message)

        # Step 2: Generate suggestion based on dialogue
        conversation = get_conversation_by_id(conversation_id)
        print(conversation.get('dialogue', ''))
        suggestion = generate_suggestion(conversation)

        return {"suggestion": suggestion}
    except Exception as e:
        return {"error": str(e)}
    
if __name__ == '__main__':
    conversation_id = "67e84ffdcdc7b8c0be4769d2"
    new_message = "How's the weather today?"
    result = update_conversation(conversation_id, new_message)
    print(result)