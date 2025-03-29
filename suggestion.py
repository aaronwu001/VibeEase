def generate_topic_suggestion(dialogue, current_speaker):
    # Organize the conversation history into a string
    conversation_history = "\n".join([f"{msg['speaker']}: {msg['content']}" for msg in dialogue])
    
    # Construct the prompt for the Gemini model
    prompt = f"""
    Here is the conversation history between A and B:
    {conversation_history}
    
    Now, {current_speaker} wants to continue the conversation. Based on the most recent part of the conversation, suggest a topic for {current_speaker} to discuss and explain how to introduce it.
    """
    
    # Use the Gemini model to generate a response (simulated here)
    topic_suggestion = get_topic_suggestion_from_gemini(prompt)
    
    return topic_suggestion


def get_topic_suggestion_from_gemini(prompt):
    # Simulate a call to the Gemini API with the constructed prompt
    # In a real implementation, you would send the prompt to Gemini and get a response
    # Here, it's a simplified example returning a suggestion
    return "You can talk about your recent travel plans, as it could help to get to know each other's interests and hobbies."


# Example dialogue:
dialogue = [
    {"speaker": "A", "content": "Hey, how's it going?"},
    {"speaker": "B", "content": "Not bad, just busy with work."},
    {"speaker": "A", "content": "Same here, work has been stressful."},
    {"speaker": "B", "content": "Yeah, it's tough to find balance these days."}
]

# Assuming it's A's turn to speak
suggestion = generate_topic_suggestion(dialogue, current_speaker="A")
print(suggestion)
