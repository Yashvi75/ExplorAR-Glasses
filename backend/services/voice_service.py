import os
import json
import google.generativeai as genai
from services import context_service, weather_service, location_service, navigation_service

# Configure Gemini
GEMINI_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
genai.configure(api_key=GEMINI_KEY)

INTENT_PROMPT = """
You are the AI brain of ExplorAR Glasses. Parse the user's natural language travel query into JSON:
- weather (needs city)
- context (needs place)
- navigation (needs source and destination)
- location (asking where they are)

Return ONLY JSON:
{
  "intent": "weather|context|navigation|location|unknown",
  "entities": {"city": "string", "place": "string", "source": "string", "destination": "string"}
}
"""

def handle_voice_query(query_text):
    try:
        model = genai.GenerativeModel('gemini-flash-latest')
        response = model.generate_content(f"{INTENT_PROMPT}\n\nUser query: {query_text}")
        
        content = response.text
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
            
        data = json.loads(content)
        intent = data.get("intent")
        entities = data.get("entities", {})

        if intent == "weather":
            city = entities.get("city")
            if city: return {"intent": "weather", "query": query_text, "response": weather_service.get_weather(city)}
            
        elif intent == "context":
            place = entities.get("place")
            if place: return {"intent": "context", "query": query_text, "response": context_service.get_context(place)}

        elif intent == "navigation":
            source = entities.get("source")
            dest = entities.get("destination")
            if source and dest: return {"intent": "navigation", "query": query_text, "response": navigation_service.get_route(source, dest)}

        return {
            "intent": intent, "query": query_text,
            "response": {"message": f"I understood your intent as '{intent}', but I need more specific details."}
        }

    except Exception as e:
        print(f"Voice Gemini Error: {e}")
        return _fallback_voice_query(query_text)

def _fallback_voice_query(query_text):
    q = query_text.lower().strip()
    if any(kw in q for kw in ["weather", "temp", "mausam"]):
        city = _extract_place(q)
        if city: return {"intent": "weather", "query": query_text, "response": weather_service.get_weather(city)}
    elif any(kw in q for kw in ["tell me", "what is", "about"]):
        place = _extract_place(q)
        if place: return {"intent": "context", "query": query_text, "response": context_service.get_context(place)}
    
    return {
        "intent": "unknown", "query": query_text,
        "response": {"message": "I'm having trouble with the AI brain right now. Can you try typing your question?"}
    }

def _extract_place(q):
    stop = ["weather", "in", "of", "at", "the", "about", "tell", "me", "what", "is", "describe"]
    words = q.split()
    place_words = [w for w in words if w not in stop and len(w) > 2]
    return " ".join(place_words).title() if place_words else None
