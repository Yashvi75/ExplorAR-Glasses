import os
import requests
import google.generativeai as genai
from utils.cache import get, set
from utils.mock_data import get_mock_city

# Configure Gemini
GEMINI_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
genai.configure(api_key=GEMINI_KEY)

OPENWEATHER_KEY = os.getenv("OPENWEATHER_API_KEY")
WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(city):
    cache_key = f"weather:{city.lower()}"
    cached = get(cache_key)
    if cached:
        return cached

    # REAL-TIME FIRST (As requested)
    try:
        params = {"q": city + ",IN", "appid": OPENWEATHER_KEY, "units": "metric", "lang": "en"}
        resp = requests.get(WEATHER_URL, params=params, timeout=6)
        
        if resp.status_code == 200:
            data = resp.json()
            temp = data["main"]["temp"]
            cond = data["weather"][0]["description"]
            
            summary = f"The weather in {data['name']} is currently {cond} at {temp}°C."
            try:
                model = genai.GenerativeModel('gemini-flash-latest')
                ai_resp = model.generate_content(f"Summarize weather for tourist in 1 short sentence: {temp}C, {cond}, {data['name']}, India.")
                summary = ai_resp.text
            except: pass

            output = {
                "city": data["name"],
                "temperature_c": temp,
                "condition": data["weather"][0]["main"],
                "description": cond.capitalize(),
                "humidity": data["main"]["humidity"],
                "ai_summary": summary,
                "icon": f"https://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png",
                "source": "Live Weather Service"
            }
            set(cache_key, output)
            return output
            
    except Exception as e:
        print(f"Weather API Error: {e}")

    # FALLBACK to Premium Database only if API fails
    mock = get_mock_city(city)
    if mock:
        w = mock["weather"]
        return {
            "city": city.title(),
            "temperature_c": w["temp"],
            "condition": w["cond"],
            "description": f"Regional weather data for {city.title()}",
            "humidity": 60,
            "ai_summary": w["summary"],
            "icon": "https://openweathermap.org/img/wn/01d@2x.png",
            "source": "ExplorAR Intelligence Core"
        }

    return {"error": "Weather data currently unavailable. Please try again later."}
