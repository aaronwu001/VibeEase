import os
import shutil
from datetime import datetime
from google import genai

## load environment variable
from dotenv import load_dotenv
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def transcribe_mp3(mp3_file):
    # Initialize the Gemini API client
    client = genai.Client(api_key=GEMINI_API_KEY)

## Get the current timestamp and create a unique filename
    timestamp = datetime.now().strftime('%Y-%m-%d%H-%M-%S')
    filename = f"mp3file{timestamp}.mp3"

## Define the folder where the file will be stored
    destination_folder = './media/'

    # Ensure the destination folder exists
    os.makedirs(destination_folder, exist_ok=True)

    # Define the full path for the new file
    destination_file_path = os.path.join(destination_folder, filename)

    # Save the MP3 file temporarily in the destination folder
    with open(destination_file_path, 'wb') as f:
        f.write(mp3_file.read()) 

    # Upload the file to Gemini
    temp_file = client.files.upload(file=destination_file_path)

## Set the transcription prompt
    prompt = 'Generate a transcript of the speech in English'

    # Call the Gemini API to transcribe the MP3 file
    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=[prompt, temp_file]
    )

## Retrieve the transcription text
    transcription = response.text

    # Delete the MP3 file after processing
    os.remove(destination_file_path)

## Return the transcription
    return transcription
