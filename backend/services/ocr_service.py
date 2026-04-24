import os
import requests


OCR_KEY = os.getenv("OCR_API_KEY")
OCR_URL = "https://api.ocr.space/parse/image"


def extract_text(image_file):
    """
    image_file: a Flask FileStorage object (from request.files)
    Returns extracted text from OCR.space API.
    """
    if not OCR_KEY:
        return {"error": "OCR_API_KEY not set in .env"}

    payload = {
        "apikey": OCR_KEY,
        "language": "eng",
        "isOverlayRequired": False,
        "OCREngine": 2,
        "detectOrientation": True,
        "scale": True,
        "isTable": False
    }

    files = {"file": (image_file.filename, image_file.stream, image_file.content_type)}
    resp = requests.post(OCR_URL, data=payload, files=files, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    if data.get("IsErroredOnProcessing"):
        return {"error": data.get("ErrorMessage", ["OCR failed"])[0]}

    parsed_results = data.get("ParsedResults", [])
    if not parsed_results:
        return {"error": "No text found in image."}

    extracted = " ".join(r["ParsedText"].strip() for r in parsed_results if r.get("ParsedText"))
    return {
        "extracted_text": extracted,
        "word_count": len(extracted.split()),
        "engine": "OCR.space Engine 2"
    }
