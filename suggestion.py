import os
import google.generativeai as genai
from dotenv import load_dotenv
from gemini_endpoint import ask_gemini

def generate_topic_suggestion(profiles, dialogue, current_speaker):
    # Organize the conversation history into a string
    conversation_history = "\n".join([f"{msg['speaker']}: {msg['content']}" for msg in dialogue])[:1800]
    
    # Construct the prompt for the Gemini model
    prompt = f"""
    You are an AI assistant that helps people communicate more smoothly and respectfully by monitoring the emotional flow of a conversation.

    You will be given:
    - Profiles of both speakers (with interests and topics they avoid)
    - A recent conversation history
    - The speaker who is about to say the next line

    Your task is to generate a short suggestion message **for the current speaker** to help them continue the conversation.

    Your suggestion should include:
    1. A quick interpretation of the other speaker’s current emotional state
    2. A judgment of whether the current topic may cause discomfort or not
    3. A recommendation:
    - If the current topic is fine → suggest continuing and give a sentence the user could say
    - If the topic should be changed → suggest a new topic (based on shared interests) and give a new starter sentence

    ✳️ Output format:
    Just two short santances in natural, supportive English, addressed to the speaker.
    Show up with three rows. 
    The first row should be a brief descriptional word of the other speaker’s current emotional state, using the format " Other's emotion is [emotion] right now."
    The seconf row should be a judgment(good/bad) of whether the current topic may cause discomfort or not. If it is a bad topic, suggest a new topic and starter sentence using the format "Please change to talk about [new topic] instead."
    The third row should be a recommendation to the speaker to either continue the conversation or suggest a new topic and starter sentence.
    Make sure it is calm, friendly, and actionable. Do **not** repeat the conversation history or profiles.

    Here is the information:

    Profiles: 
    {str(profiles)}

    Here is the conversation history between A and B:
    {conversation_history}
    
    Now, {current_speaker} wants to continue the conversation. Based on the most recent part of the conversation, suggest a topic for {current_speaker} to discuss and explain how to introduce it.
    """

    # testing code
    with open('curr_prompt.txt', 'w') as file:
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

    # Testing Cases:
    # profiles = {
    #     'A': {
    #         'interests': ['photography', 'cooking', 'travel'],
    #         'avoid': ['politics']
    #     },
    #     'B': {
    #         'interests': ['cooking', 'tech startups', 'travel'],
    #         'avoid': ['sports']
    #     }
    # }

    # dialogue = [
    #     {"speaker": "A", "content": "I tried a new pasta recipe yesterday, it turned out amazing."},
    #     {"speaker": "B", "content": "That sounds great! What kind of sauce did you use?"}
    # ]
    # current_speaker = "A"


    # Assuming it's A's turn to speak
    suggestion = generate_topic_suggestion(profiles, dialogue, current_speaker="A")
    print(suggestion)
    
    # testing code
    with open('suggestion.txt', 'w') as file:
        file.write(suggestion)  # Write the string to the file
