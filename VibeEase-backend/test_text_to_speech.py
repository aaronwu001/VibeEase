# testing_script.py

# Import the function to be tested
from text_to_speech import transcribe_mp3  # Replace 'your_module' with the actual module name where your function is located

# Define the path to your pre-existing MP3 file
mp3_file_path = './test_media/Test2.mp3'  


# Open the MP3 file in binary read mode
with open(mp3_file_path, 'rb') as f:
    mp3_file = f  # Pass the file object to the function

    # Call the transcribe_mp3 function and get the transcription result
    transcription = transcribe_mp3(mp3_file)

    # Print the transcription result
    print("Transcription Result:")
    print(transcription)
