from pydub import AudioSegment
import io
from werkzeug.datastructures import FileStorage
from flask import send_file

def change_mp3(file):
    """Convert an uploaded audio file to MP3 format."""
    try:
        # Read raw bytes
        audio_stream = io.BytesIO(file.read()) 

        # Detect format from MIME type or filename
        filename = file.filename.lower()
        format_type = filename.split(".")[-1]  # Get file extension

        # Convert format if supported
        if format_type not in ["wav", "webm", "ogg", "m4a"]:
            print("Unsupported format:", format_type)
            return None
        
        audio = AudioSegment.from_file(audio_stream, format=format_type)

        # Convert to MP3
        mp3_stream = io.BytesIO()
        audio.export(mp3_stream, format="mp3")

        mp3_stream.seek(0)  # Reset position

        # Create a FileStorage object from the BytesIO stream
        mp3_file = FileStorage(mp3_stream, filename="converted.mp3")

        # Return the FileStorage object as a Flask response with the correct MIME type
        return send_file(mp3_file, mimetype="audio/mpeg")

    except Exception as e:
        print(f"Error converting file to MP3: {e}")
        return None
