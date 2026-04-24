from flask import Blueprint, jsonify, request
from services import voice_service

voice_bp = Blueprint("voice", __name__)


@voice_bp.route("/voice/query", methods=["POST"])
def voice_query():
    body = request.get_json(silent=True) or {}
    query = body.get("query", "").strip()

    if not query:
        return jsonify({"error": "'query' field with transcribed text is required"}), 400

    try:
        result = voice_service.handle_voice_query(query)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
