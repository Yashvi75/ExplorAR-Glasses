from flask import Blueprint, jsonify, request
from services import weather_service

weather_bp = Blueprint("weather", __name__)


@weather_bp.route("/weather", methods=["GET"])
def get_weather():
    city = request.args.get("city", "").strip()
    if not city:
        return jsonify({"error": "'city' query parameter is required. e.g. ?city=Kota"}), 400
    try:
        result = weather_service.get_weather(city)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
