from gemini_endpoint import ask_gemini

def generate_topic_suggestion(conversation):
    # Organize the conversation history into a string
    dialogue = "\n".join(conversation.get('dialogue', ''))[:1800]
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
    
    Now, one user wants to continue the conversation. Based on the most recent part of the conversation, suggest a topic for {current_speaker} to discuss and explain how to introduce it.
    """

    # Use the Gemini model to generate a response (simulated here)
    topic_suggestion = get_topic_suggestion_from_gemini(prompt)
    
    return topic_suggestion


def get_topic_suggestion_from_gemini(prompt):
    # call Gemini API with the constructed prompt
    response = ask_gemini(prompt)
    return response.text


def update_conversation(conversation_id, new_message):
    
    # get conversation by conversation_id from Mongo DB
    conversation = get_conversation_by_id(conversation_id)

    # add new message to the conversation dialogue
    add_new_message(conversation_id, new_message)

    # generate suggestion for the current conversation 
    generate_topic_suggestion(conversation) 

    suggestion = generate_topic_suggestion(profiles, dialogue, current_speaker)
    return suggestion


if __name__ == '__main__':
    # Initial dialogue setup
    dialogue = [
        "Hey, how's it going?",
        "Not bad, just busy with work.",
        "Same here, work has been stressful.",
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
    
    # Simulate a new message
    new_message = "Yeah, it's tough to find balance these days."
    current_speaker = "A"
    
    # Update conversation and generate a new topic suggestion
    suggestion = update_conversation(dialogue, new_message, current_speaker)
    
    # Output the suggestion
    print(suggestion)
    
    # Optionally, save suggestion to a file for testing purposes
    with open('test_output/suggestion.txt', 'w') as file:
        file.write(suggestion)  # Write the string to the file
