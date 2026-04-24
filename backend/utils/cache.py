import json
import os
import time

CACHE_FILE = os.path.join(os.path.dirname(__file__), "../data/cache.json")
CACHE_TTL = 600  # seconds (10 minutes)


def _load():
    try:
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _save(data):
    with open(CACHE_FILE, "w") as f:
        json.dump(data, f, indent=2)


def get(key):
    store = _load()
    entry = store.get(key)
    if entry:
        if time.time() - entry["ts"] < CACHE_TTL:
            return entry["value"]
    return None


def set(key, value):
    store = _load()
    store[key] = {"value": value, "ts": time.time()}
    _save(store)


def clear():
    _save({})
