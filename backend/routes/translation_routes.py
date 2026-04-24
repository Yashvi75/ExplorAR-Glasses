from flask import Blueprint, jsonify, request
from services import translation_service

translation_bp = Blueprint("translation", __name__)


@translation_bp.route("/translate", methods=["POST"])
def translate():
    body = request.get_json(silent=True) or {}
    text = body.get("text", "").strip()
    target = body.get("target_language", "").strip()

    if not text:
        return jsonify({"error": "'text' field is required in JSON body"}), 400
    if not target:
        return jsonify({"error": "'target_language' field is required. e.g. 'hi' for Hindi"}), 400

    try:
        result = translation_service.translate_text(text, target)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@translation_bp.route("/translate/detect", methods=["POST"])
def detect():
    body = request.get_json(silent=True) or {}
    text = body.get("text", "").strip()
    if not text:
        return jsonify({"error": "'text' field is required"}), 400
    try:
        result = translation_service.detect_language(text)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@translation_bp.route("/translate/languages", methods=["GET"])
def languages():
    try:
        result = translation_service.supported_languages()
        return jsonify({"languages": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
