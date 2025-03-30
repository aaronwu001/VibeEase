from flask import Flask, request, jsonify
from flask_cors import CORS #Import CORS
from werkzeug.utils import secure_filename
import tempfile
import os
import sys
sys.path.append(os.path.abspath("db"))
from conversation import create_conversation, add_dialogue, remove_conversation

app = Flask(__name__)
CORS(app)

# Placeholder: speech-to-text conversion using Gemini
def speech_to_text(audio_path):
    # TODO: Replace with actual Gemini STT call
    return "This is transcribed text from voice."

# Placeholder: AI suggestion generator (e.g. Gemini chatbot)
def generate_suggestion(text):
    # TODO: Replace with actual Gemini call
    return f"Suggested reply to: '{text}'"

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

    try:
        # Check if the file is valid
        if not voice_file:
            return jsonify({"error": "No file uploaded"}), 400
        
        # Optionally, you can check the file's type (e.g., ensure it's an MP3 or WAV)
        if 'audio' not in voice_file.content_type:
            return jsonify({"error": "File is not an audio file"}), 400
        
        # Save voice file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            voice_file.save(temp_audio.name)
            audio_path = temp_audio.name

        # Step 1: Speech to Text (placeholder)
        text = speech_to_text(audio_path)
        print(f"Transcribed text: {text}")

        # Step 2: Update conversation in MongoDB
        add_dialogue(conversation_id, text)

        # Step 3: Generate suggestion based on dialogue
        suggestion = generate_suggestion(text)

        # Cleanup temp file
        os.remove(audio_path)

        return jsonify({"suggestion": suggestion})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

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
