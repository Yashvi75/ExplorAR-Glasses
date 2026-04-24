import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def test_gemini():
    key = os.getenv("GOOGLE_MAPS_API_KEY")
    print(f"Testing Gemini with key: {key[:10]}...")
    try:
        genai.configure(api_key=key)
        model = genai.GenerativeModel('gemini-flash-latest')
        response = model.generate_content("Hello, respond with 'SUCCESS'")
        print(f"Gemini Result: {response.text}")
    except Exception as e:
        print(f"Gemini Error: {e}")

def test_weather():
    key = os.getenv("OPENWEATHER_API_KEY")
    import requests
    url = f"http://api.openweathermap.org/data/2.5/weather?q=Kota,IN&appid={key}"
    print(f"Testing Weather with key: {key[:10]}...")
    try:
        r = requests.get(url)
        print(f"Weather Result: {r.status_code} {r.json().get('name')}")
    except Exception as e:
        print(f"Weather Error: {e}")

if __name__ == "__main__":
    test_gemini()
    test_weather()
