import os
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up static folder path to the frontend directory
frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../frontend"))

app = Flask(__name__, static_folder=frontend_dir)
CORS(app)

# ─── Frontend Routes ───────────────────────────────────────────────────────────
@app.route("/")
def index():
    return send_from_directory(frontend_dir, "index.html")

@app.route("/<path:path>")
def static_proxy(path):
    return send_from_directory(frontend_dir, path)

# ─── Register Blueprints ───────────────────────────────────────────────────────
from routes.location_routes import location_bp
from routes.context_routes import context_bp
from routes.navigation_routes import navigation_bp
from routes.weather_routes import weather_bp
from routes.translation_routes import translation_bp
from routes.ocr_routes import ocr_bp
from routes.voice_routes import voice_bp

# Note: We prefix API routes to avoid conflict with frontend files
app.register_blueprint(location_bp, url_prefix="/api")
app.register_blueprint(context_bp, url_prefix="/api")
app.register_blueprint(navigation_bp, url_prefix="/api")
app.register_blueprint(weather_bp, url_prefix="/api")
app.register_blueprint(translation_bp, url_prefix="/api")
app.register_blueprint(ocr_bp, url_prefix="/api")
app.register_blueprint(voice_bp, url_prefix="/api")

# ─── Health / System Status ───────────────────────────────────────────────────
@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "running",
        "modules": ["location", "context", "navigation", "weather", "translation", "ocr", "voice"],
        "project": "ExplorAR Glasses Backend",
        "version": "2.0.0"
    })

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("DEBUG", "true").lower() == "true"
    print(f"\n[ExplorAR] System running on http://localhost:{port}\n")
    app.run(debug=debug, port=port)
