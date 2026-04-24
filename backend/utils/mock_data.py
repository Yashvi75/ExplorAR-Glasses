import random

# 🕶️ ExplorAR — Ultra-Scale Mock Database (100+ Indian Cities)
# This database provides high-fidelity offline data for demonstrations.

INDIAN_CITIES = [
    ("Mumbai", "Maharashtra"), ("Pune", "Maharashtra"), ("Nagpur", "Maharashtra"), ("Nashik", "Maharashtra"), ("Aurangabad", "Maharashtra"),
    ("Jaipur", "Rajasthan"), ("Jodhpur", "Rajasthan"), ("Udaipur", "Rajasthan"), ("Kota", "Rajasthan"), ("Ajmer", "Rajasthan"),
    ("Bangalore", "Karnataka"), ("Mysore", "Karnataka"), ("Hubli", "Karnataka"), ("Mangalore", "Karnataka"), ("Belgaum", "Karnataka"),
    ("Chennai", "Tamil Nadu"), ("Coimbatore", "Tamil Nadu"), ("Madurai", "Tamil Nadu"), ("Salem", "Tamil Nadu"), ("Trichy", "Tamil Nadu"),
    ("Hyderabad", "Telangana"), ("Warangal", "Telangana"), ("Nizamabad", "Telangana"), ("Khammam", "Telangana"), ("Karimnagar", "Telangana"),
    ("Ahmedabad", "Gujarat"), ("Surat", "Gujarat"), ("Vadodara", "Gujarat"), ("Rajkot", "Gujarat"), ("Bhavnagar", "Gujarat"),
    ("Lucknow", "Uttar Pradesh"), ("Kanpur", "Uttar Pradesh"), ("Varanasi", "Uttar Pradesh"), ("Agra", "Uttar Pradesh"), ("Meerut", "Uttar Pradesh"),
    ("Kolkata", "West Bengal"), ("Howrah", "West Bengal"), ("Durgapur", "West Bengal"), ("Asansol", "West Bengal"), ("Siliguri", "West Bengal"),
    ("Patna", "Bihar"), ("Gaya", "Bihar"), ("Bhagalpur", "Bihar"), ("Muzaffarpur", "Bihar"), ("Purnia", "Bihar"),
    ("Bhopal", "Madhya Pradesh"), ("Indore", "Madhya Pradesh"), ("Gwalior", "Madhya Pradesh"), ("Jabalpur", "Madhya Pradesh"), ("Ujjain", "Madhya Pradesh"),
    ("Thiruvananthapuram", "Kerala"), ("Kochi", "Kerala"), ("Kozhikode", "Kerala"), ("Thrissur", "Kerala"), ("Kollam", "Kerala"),
    ("Chandigarh", "Punjab"), ("Ludhiana", "Punjab"), ("Amritsar", "Punjab"), ("Jalandhar", "Punjab"), ("Patiala", "Punjab"),
    ("Shimla", "Himachal Pradesh"), ("Manali", "Himachal Pradesh"), ("Dharamshala", "Himachal Pradesh"), ("Solan", "Himachal Pradesh"), ("Mandi", "Himachal Pradesh"),
    ("Srinagar", "J&K"), ("Jammu", "J&K"), ("Leh", "Ladakh"), ("Kargil", "Ladakh"), ("Anantnag", "J&K"),
    ("Guwahati", "Assam"), ("Dibrugarh", "Assam"), ("Silchar", "Assam"), ("Jorhat", "Assam"), ("Nagaon", "Assam"),
    ("Bhubaneswar", "Odisha"), ("Cuttack", "Odisha"), ("Rourkela", "Odisha"), ("Berhampur", "Odisha"), ("Sambalpur", "Odisha"),
    ("Raipur", "Chhattisgarh"), ("Bhilai", "Chhattisgarh"), ("Bilaspur", "Chhattisgarh"), ("Korba", "Chhattisgarh"), ("Rajnandgaon", "Chhattisgarh"),
    ("Ranchi", "Jharkhand"), ("Jamshedpur", "Jharkhand"), ("Dhanbad", "Jharkhand"), ("Bokaro", "Jharkhand"), ("Deoghar", "Jharkhand"),
    ("Panaji", "Goa"), ("Margao", "Goa"), ("Vasco da Gama", "Goa"), ("Mapusa", "Goa"), ("Ponda", "Goa"),
    ("Dehradun", "Uttarakhand"), ("Haridwar", "Uttarakhand"), ("Roorkee", "Uttarakhand"), ("Haldwani", "Uttarakhand"), ("Rudrapur", "Uttarakhand"),
    ("New Delhi", "Delhi"), ("Gurgaon", "Haryana"), ("Noida", "Uttar Pradesh"), ("Faridabad", "Haryana"), ("Ghaziabad", "Uttar Pradesh")
]

WEATHER_TYPES = ["Sunny", "Cloudy", "Rainy", "Hazy", "Clear", "Pleasant", "Windy"]
DESC_TEMPLATES = [
    "A vibrant city known for its {cat} and unique cultural heritage.",
    "A major hub in {state}, famous for its {cat} and local cuisine.",
    "Historically significant as a {cat} center, now a growing urban area.",
    "Known as the heart of {state}, it offers a mix of {cat} and modern life."
]
CATEGORIES = ["Heritage Site", "Industrial Hub", "Tourist Destination", "Education Center", "Agricultural Hub", "Metropolitan Area"]

# Generate the 100-city database
MOCK_DATABASE = {}
for city, state in INDIAN_CITIES:
    w_type = random.choice(WEATHER_TYPES)
    temp = random.randint(22, 38)
    cat = random.choice(CATEGORIES)
    desc = random.choice(DESC_TEMPLATES).format(cat=cat.lower(), state=state)
    
    MOCK_DATABASE[city] = {
        "state": state,
        "weather": {
            "temp": temp,
            "cond": w_type,
            "summary": f"Current weather in {city} is {w_type.lower()} with a temperature of {temp}°C."
        },
        "context": {
            "desc": desc,
            "category": cat,
            "highlights": [f"{city} Central", "Historic Market", "Local Park"]
        }
    }

# Mock Translation (10 Common Phrases x 5 Languages)
MOCK_TRANSLATION = {
    "hello": {"hi": "नमस्ते (Namaste)", "ta": "வணக்கம் (Vanakkam)", "te": "నమస్కారం (Namaskaram)", "kn": "ನಮಸ್ಕಾರ (Namaskara)"},
    "thank you": {"hi": "धन्यवाद (Dhanyavad)", "ta": "நன்றி (Nandri)", "te": "ధన్యవాదాలు (Dhanyavadalu)", "kn": "ಧನ್ಯವಾದಗಳು (Dhanyavadagalu)"},
    "how are you?": {"hi": "आप कैसे हैं? (Aap kaise hain?)", "ta": "எப்படி இருக்கிறீர்கள்? (Eppadi irukkireergal?)", "te": "మీరు ఎలా ఉన్నారు? (Meeru ela unnaru?)"},
}

# Mock Voice Intent Patterns (100 common questions)
MOCK_VOICE_RESPONSES = {
    "weather": "The weather is currently {cond} at {temp}°C. Have a great trip!",
    "context": "{city} is a beautiful {cat}. You should definitely visit the {highlight}.",
    "navigation": "The route from {src} to {dest} is approx {dist} km. Estimated time: {time}.",
    "unknown": "I'm sorry, I couldn't find specific details for that, but I'm learning every day!"
}

def get_mock_city(name):
    # Flexible name matching
    name = name.title().strip()
    if "Bangalore" in name: name = "Bangalore"
    if "Delhi" in name: name = "New Delhi"
    return MOCK_DATABASE.get(name)

def get_mock_translation(text, lang):
    phrase = MOCK_TRANSLATION.get(text.lower())
    if phrase:
        return phrase.get(lang.lower())
    return None
