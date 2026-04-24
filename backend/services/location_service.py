import requests
from utils.cache import get, set

# Free Alternative: Nominatim (OpenStreetMap)
NOMINATIM_REVERSE_URL = "https://nominatim.openstreetmap.org/reverse"

def reverse_geocode(lat, lon):
    cache_key = f"loc:{lat}:{lon}"
    cached = get(cache_key)
    if cached:
        return cached

    try:
        headers = {'User-Agent': 'ExplorAR-Travel-Assistant/1.0'}
        params = {
            "lat": lat,
            "lon": lon,
            "format": "json"
        }
        resp = requests.get(NOMINATIM_REVERSE_URL, params=params, headers=headers)
        resp.raise_for_status()
        data = resp.json()

        addr = data.get("address", {})
        city = addr.get("city") or addr.get("town") or addr.get("village") or "Unknown"
        state = addr.get("state", "India")
        
        output = {
            "address": data.get("display_name"),
            "city": city,
            "state": state,
            "engine": "Nominatim (OpenSource)"
        }
        
        set(cache_key, output)
        return output
    except Exception as e:
        print(f"Nominatim Error: {e}")
        return {"error": "Location service error."}
