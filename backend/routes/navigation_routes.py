from flask import Blueprint, jsonify, request
from services import navigation_service

navigation_bp = Blueprint("navigation", __name__)

VALID_MODES = {"driving", "walking", "bicycling", "transit"}


@navigation_bp.route("/navigation", methods=["GET"])
def navigate():
    source = request.args.get("source", "").strip()
    destination = request.args.get("destination", "").strip()
    mode = request.args.get("mode", "driving").strip().lower()

    if not source or not destination:
        return jsonify({"error": "'source' and 'destination' query parameters are required"}), 400
    if mode not in VALID_MODES:
        return jsonify({"error": f"Invalid mode. Choose from: {', '.join(VALID_MODES)}"}), 400

    try:
        result = navigation_service.get_route(source, destination, mode)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
