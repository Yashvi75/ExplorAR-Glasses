import os
import requests
import google.generativeai as genai
from utils.cache import get, set
from utils.mock_data import get_mock_city

# Configure Gemini
GEMINI_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
genai.configure(api_key=GEMINI_KEY)

NOMINATIM_SEARCH_URL = "https://nominatim.openstreetmap.org/search"
WIKI_API_URL = "https://en.wikipedia.org/w/api.php"

def get_context(place):
    cache_key = f"context:{place.lower()}"
    cached = get(cache_key)
    if cached:
        return cached

    # Check Mock Data first
    mock = get_mock_city(place)
    if mock:
        ctx = mock["context"]
        return {
            "place": place.title(),
            "description": ctx["desc"],
            "category": ctx["category"],
            "rating": 4.8,
            "nearby_highlights": ctx["highlights"],
            "engine": "ExplorAR Intelligence Core"
        }

    description = ""
    category = "landmark"
    
    try:
        headers = {'User-Agent': 'ExplorAR-Travel-Assistant/1.0'}
        params = {"q": place + " India", "format": "json", "addressdetails": 1, "limit": 1}
        resp = requests.get(NOMINATIM_SEARCH_URL, params=params, headers=headers, timeout=5)
        results = resp.json()
        if results:
            category = results[0].get("type", "landmark")

        wiki_params = {"action": "query", "format": "json", "titles": place, "prop": "extracts", "exintro": True, "explaintext": True, "redirects": 1}
        wiki_resp = requests.get(WIKI_API_URL, params=wiki_params, timeout=5)
        pages = wiki_resp.json().get("query", {}).get("pages", {})
        for page_id in pages:
            if page_id != "-1":
                description = pages[page_id].get("extract", "")
                break

        if len(description) < 100:
            try:
                model = genai.GenerativeModel('gemini-flash-latest')
                ai_resp = model.generate_content(f"Provide a 2-3 sentence travel description for '{place}' in India.")
                description = ai_resp.text
            except:
                if not description: description = f"No description available for {place}."

        output = {
            "place": place,
            "description": description,
            "category": category,
            "rating": None,
            "nearby_highlights": ["Local Landmarks", "Historical Sites"],
            "engine": "OSM + Wiki + Gemini"
        }
        set(cache_key, output)
        return output
    except Exception as e:
        return {"error": f"Context unavailable: {str(e)}"}
