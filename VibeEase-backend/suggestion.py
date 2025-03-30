from gemini_endpoint import ask_gemini

def generate_topic_suggestion(profiles, dialogue, current_speaker):
    # Organize the conversation history into a string
    conversation_history = "\n".join([f"{msg['speaker']}: {msg['content']}" for msg in dialogue])[:1800]
    
    # Construct the prompt for the Gemini model
    prompt = f"""

    You are an AI assistant that helps people communicate more smoothly by monitoring the emotional flow of a conversation.
    Your response must be within one sentence.
    
    You will be given:
    - Profiles: the two speakers' interests and topics they avoid
    - Profile B: their interests and topics they avoid
    - A short conversation history between the two users

    Your tasks:
    1. Identify the current emotional state of both users (choose from: happy, neutral, sad, stressed, confused, frustrated).
    2. Determine if the current topic may cause discomfort or a negative reaction.
    3. Decide whether to continue the current topic or redirect the conversation.
    4. If redirection is needed, suggest a new topic based on shared interests and provide a starter sentence.
    5. Provide a short explanation of your reasoning.

    Profiles: 
    {str(profiles)}

    Here is the conversation history between A and B:
    {conversation_history}
    
    Now, {current_speaker} wants to continue the conversation. Based on the most recent part of the conversation, suggest a topic for {current_speaker} to discuss and explain how to introduce it.
    """

    # testing code
    with open('test_output/curr_prompt.txt', 'w') as file:
        file.write(prompt)  # Write the string to the file

    # Use the Gemini model to generate a response (simulated here)
    topic_suggestion = get_topic_suggestion_from_gemini(prompt)
    
    return topic_suggestion


def get_topic_suggestion_from_gemini(prompt):
    # call Gemini API with the constructed prompt
    
    response = ask_gemini(prompt)
    return response.text

    # return "You can talk about your recent travel plans, as it could help to get to know each other's interests and hobbies."

if __name__ == '__main__':

    # Example dialogue:
    dialogue = [
        {"speaker": "A", "content": "Hey, how's it going?"},
        {"speaker": "B", "content": "Not bad, just busy with work."},
        {"speaker": "A", "content": "Same here, work has been stressful."},
        {"speaker": "B", "content": "Yeah, it's tough to find balance these days."}
    ]

    profiles = {
        'A': {
            'interests': ['hiking', 'dogs', 'AI'],
            'avoid': ['family', 'relationships']
        },
        'B': {
            'interests': ['hiking', 'cooking', 'dogs'],
            'avoid': ['politics', 'breakups']
        }
    }

    # Assuming it's A's turn to speak
    suggestion = generate_topic_suggestion(profiles, dialogue, current_speaker="A")
    print(suggestion)
    
    # testing code
    with open('test_output/suggestion.txt', 'w') as file:
        file.write(suggestion)  # Write the string to the file
