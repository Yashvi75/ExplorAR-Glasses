from flask import Blueprint, jsonify, request
from services import ocr_service

ocr_bp = Blueprint("ocr", __name__)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "bmp", "tiff", "webp"}


def _allowed(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@ocr_bp.route("/ocr", methods=["POST"])
def ocr():
    if "image" not in request.files:
        return jsonify({"error": "No image file uploaded. Use key 'image' in form-data."}), 400

    file = request.files["image"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400
    if not _allowed(file.filename):
        return jsonify({"error": f"Invalid file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"}), 400

    try:
        result = ocr_service.extract_text(file)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
