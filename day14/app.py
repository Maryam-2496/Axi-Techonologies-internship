import os
from flask import Flask, jsonify
from dotenv import load_dotenv
from models.user_model import db
from routes.auth_routes import auth_bp
from flask_talisman import Talisman
from extensions import limiter
from flasgger import Swagger
from extensions import limiter, redis_client, task_queue, socketio
import socket_events

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

app = Flask(__name__)

csp = {
    "default-src": "'self'",
    "script-src": ["'self'", "'unsafe-inline'", "cdn.jsdelivr.net"],
    "style-src": [
        "'self'",
        "'unsafe-inline'",
        "fonts.googleapis.com",
        "cdn.jsdelivr.net",
    ],
    "font-src": ["'self'", "fonts.gstatic.com"],
}
Talisman(app, force_https=False, content_security_policy=csp)
swagger = Swagger(app)
limiter.init_app(app)
socketio.init_app(app)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"sqlite:///{os.path.join(BASE_DIR, 'users.db')}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
app.register_blueprint(auth_bp)

with app.app_context():
    db.create_all()


@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Resource not found"}), 404


@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    socketio.run(
        app, port=3000, debug=False, use_reloader=False, allow_unsafe_werkzeug=True
    )
    # socketio.run(app, port=3000, debug=False, use_reloader=False)
    # socketio.run(app, port=3000, debug=True)
