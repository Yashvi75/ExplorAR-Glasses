import requests
from utils.cache import get, set

# Free Alternative: OSRM (Open Source Routing Machine)
OSRM_URL = "http://router.project-osrm.org/route/v1/driving"
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"

def get_route(source, destination, mode="driving"):
    cache_key = f"nav:{source.lower()}:{destination.lower()}"
    cached = get(cache_key)
    if cached:
        return cached

    try:
        headers = {'User-Agent': 'ExplorAR-Travel-Assistant/1.0'}
        src_resp = requests.get(NOMINATIM_URL, params={"q": source, "format": "json", "limit": 1}, headers=headers)
        dest_resp = requests.get(NOMINATIM_URL, params={"q": destination, "format": "json", "limit": 1}, headers=headers)
        
        if not src_resp.json() or not dest_resp.json():
            return {"error": "Could not find coordinates for source or destination."}
            
        src_coords = f"{src_resp.json()[0]['lon']},{src_resp.json()[0]['lat']}"
        dest_coords = f"{dest_resp.json()[0]['lon']},{dest_resp.json()[0]['lat']}"

        route_url = f"{OSRM_URL}/{src_coords};{dest_coords}"
        params = {"overview": "full", "steps": "true", "geometries": "geojson"}
        
        resp = requests.get(route_url, params=params)
        resp.raise_for_status()
        data = resp.json()

        if data.get("code") != "Ok":
            return {"error": "No route found."}

        route = data["routes"][0]
        distance_km = round(route["distance"] / 1000, 1)
        duration_min = round(route["duration"] / 60)

        # Match frontend expectations:
        steps = []
        for leg in route["legs"]:
            for step in leg["steps"]:
                instr = step.get("maneuver", {}).get("type", "Proceed")
                modifier = step.get("maneuver", {}).get("modifier", "")
                name = step.get("name", "Road")
                dist = round(step.get("distance", 0))
                
                steps.append({
                    "instruction": f"{instr.capitalize()} {modifier} onto {name}".strip(),
                    "distance": f"{dist} m",
                    "duration": f"{round(step.get('duration', 0))}s"
                })

        output = {
            "source": source,
            "destination": destination,
            "total_distance": f"{distance_km} km",
            "total_duration": f"{duration_min} mins",
            "steps": steps[:15], 
            "engine": "ExplorAR Routing Engine"
        }
        
        set(cache_key, output)
        return output

    except Exception as e:
        print(f"OSRM Error: {e}")
        return {"error": "Navigation service error."}
