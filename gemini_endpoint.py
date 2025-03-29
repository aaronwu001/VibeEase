from google import genai

# load environment variable 
from dotenv import load_dotenv
import os
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def ask_gemini(query):

    client = genai.Client(api_key=GEMINI_API_KEY)

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=query,
    )

    return response

if __name__ == '__main__':
    test_query = "Explain how AI works"
    response = ask_gemini(test_query)
    print(response.text)
