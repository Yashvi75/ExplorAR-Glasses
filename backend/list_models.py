import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def list_models():
    key = os.getenv("GOOGLE_MAPS_API_KEY")
    print(f"Listing models with key: {key[:10]}...")
    try:
        genai.configure(api_key=key)
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(m.name)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    list_models()
