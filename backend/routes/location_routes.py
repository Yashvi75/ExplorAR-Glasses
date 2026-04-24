from flask import Blueprint, jsonify, request
from services import location_service

location_bp = Blueprint("location", __name__)


@location_bp.route("/location/reverse-geocode", methods=["GET"])
def reverse_geocode():
    lat = request.args.get("lat")
    lng = request.args.get("lng")
    if not lat or not lng:
        return jsonify({"error": "lat and lng query parameters are required"}), 400
    try:
        result = location_service.reverse_geocode(float(lat), float(lng))
        return jsonify(result)
    except ValueError:
        return jsonify({"error": "lat and lng must be valid numbers"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
