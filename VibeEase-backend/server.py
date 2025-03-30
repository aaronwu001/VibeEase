from flask import Flask, request, jsonify
from flask_cors import CORS #Import CORS
from werkzeug.utils import secure_filename
import tempfile
import os
import sys
sys.path.append(os.path.abspath("db"))
from conversation import create_conversation, add_dialogue, remove_conversation
from update_convo import update_conversation
from text_to_speech import transcribe_mp3

app = Flask(__name__)
CORS(app)

# Placeholder: speech-to-text conversion using Gemini
def speech_to_text(audio_path):
    # TODO: Replace with actual Gemini STT call
    return "This is transcribed text from voice."

# Route 1: Start a new conversation
@app.route("/start_conversation", methods=["POST"])
def start_conversation():
    data = request.get_json()  # Parse JSON data

    if not data:
        return "No JSON data provided", 400  # Bad Request

    user1_id = data.get("user_id")
    user2_id = data.get("other_user_id")

    if not user1_id or not user2_id:
        return jsonify({"error": "user_id and other_user_id are required"}), 400

    try: 
        conversation_id = create_conversation(user1_id, user2_id)
        return jsonify({"conversation_id": str(conversation_id)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route 2: Update conversation (every 10s)
@app.route("/update_conversation", methods=["POST"])
def update_conversation():
    print('request', request)
    print('updating conversation now')
    conversation_id = request.form.get("conversation_id")
    voice_file = request.files.get("new_dialogue")

    print("convo id", conversation_id)
    print("voice file", voice_file)

    if not conversation_id or not voice_file:
        return jsonify({"error": "conversation_id and new_dialogue (voice) are required"}), 400

    # Check if the MP3 file is provided
    mp3_file = request.files.get("new_dialogue")
    if not mp3_file:
        return jsonify({"error": "MP3 file (new_dialogue) is required"}), 400

    try:
        # Step 1: Transcribe the MP3 file
        new_dialogue = transcribe_mp3(mp3_file)

        # Step 2: Update the conversation
        update_result = update_conversation(new_dialogue)

        # Step 3: Check if the update contains a suggestion and return it
        if "suggestion" in update_result:
            suggestion = update_result.get("suggestion")
            return jsonify({"suggestion": suggestion}), 200
        else:
            # If there's no suggestion, return an error
            return jsonify({"error": "No suggestion found in the update result"}), 400

    except ValueError as e:
        # Catch specific errors related to the transcription or conversation update
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        # Catch any other unexpected errors
        return jsonify({"error": "An unexpected error occurred: " + str(e)}), 500

# Route 3: End conversation
@app.route("/end_conversation", methods=["POST"])
def end_conversation():
    data = request.get_json()
    conversation_id = data.get("conversation_id")

    if not conversation_id:
        return jsonify({"error": "conversation_id is required"}), 400

    try:
        remove_conversation(conversation_id)
        return jsonify({"status": "conversation ended"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)