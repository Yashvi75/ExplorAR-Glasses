from flask import Blueprint, jsonify, request
from services import context_service

context_bp = Blueprint("context", __name__)


@context_bp.route("/context", methods=["GET"])
def get_context():
    place = request.args.get("place", "").strip()
    if not place:
        return jsonify({"error": "'place' query parameter is required. e.g. ?place=Kota"}), 400
    try:
        result = context_service.get_context(place)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
