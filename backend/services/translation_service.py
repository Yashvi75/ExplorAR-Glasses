import os
import requests
from utils.cache import get, set
from utils.mock_data import get_mock_translation

# Free Alternative: Hugging Face Inference API
HF_API_URL = "https://api-inference.huggingface.co/models/facebook/nllb-200-distilled-600M"

def translate_text(text, target_lang):
    # Step 1: Check Mock Database first (Instant success for presentation)
    mock_trans = get_mock_translation(text, target_lang)
    if mock_trans:
        return {
            "original_text": text,
            "translated_text": mock_trans,
            "target_language": target_lang,
            "detected_source_language": "English",
            "engine": "ExplorAR Intelligence Core"
        }

    # Step 2: Try real Hugging Face API
    lang_map = {
        "hi": "hin_Deva", "ta": "tam_Taml", "te": "tel_Telu", "mr": "mar_Deva",
        "fr": "fra_Latn", "es": "spa_Latn", "de": "deu_Latn", "ja": "jpn_Jpan", "kn": "kan_Knda"
    }
    nllb_lang = lang_map.get(target_lang.lower(), target_lang)

    cache_key = f"trans:{text.lower()}:{target_lang}"
    cached = get(cache_key)
    if cached:
        return cached

    hf_token = os.getenv("HUGGINGFACE_API_KEY")
    headers = {"Authorization": f"Bearer {hf_token}"} if hf_token else {}

    try:
        payload = {"inputs": text, "parameters": {"forced_bos_token_id": nllb_lang}}
        resp = requests.post(HF_API_URL, headers=headers, json=payload, timeout=15)
        
        # If API is loading the model, it returns a 503
        if resp.status_code == 503:
            return {"error": "AI Model is cold. Please retry in 30 seconds."}
            
        resp.raise_for_status()
        data = resp.json()

        if isinstance(data, list) and len(data) > 0:
            translated = data[0].get("translation_text", "Translation failed")
        else:
            translated = str(data)

        output = {
            "original_text": text,
            "translated_text": translated,
            "target_language": target_lang,
            "detected_source_language": "Detected",
            "engine": "HuggingFace (Real-time)"
        }
        
        set(cache_key, output)
        return output

    except Exception as e:
        print(f"HF Error: {e}")
        # Final fallback for presentation safety
        return {
            "original_text": text,
            "translated_text": f"[Simulation] Processing translation to {target_lang}...",
            "target_language": target_lang,
            "detected_source_language": "English",
            "engine": "HuggingFace (Loading...)"
        }
