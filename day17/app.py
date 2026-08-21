import os
from flask import Flask, jsonify, request
from dotenv import load_dotenv
from models.user_model import db
from routes.auth_routes import auth_bp
from routes.health_routes import health_bp
from flask_talisman import Talisman
from prometheus_flask_exporter import PrometheusMetrics
from flasgger import Swagger
from extensions import limiter, redis_client, task_queue, socketio  # noqa: F401
import socket_events  # noqa: F401
from middleware.correlation_middleware import register_correlation_id
import logging
from concurrent_log_handler import ConcurrentRotatingFileHandler
from pythonjsonlogger import jsonlogger
from tasks import slow_operation
from tasks import generate_invoice
from rq import Retry


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter(
    "%(asctime)s %(levelname)s %(name)s %(correlation_id)s %(message)s"
)
logHandler.setFormatter(formatter)

fileHandler = ConcurrentRotatingFileHandler(
    os.path.join(BASE_DIR, "app.log"), maxBytes=1_000_000, backupCount=5
)
fileHandler.setFormatter(formatter)

logger = logging.getLogger()
logger.addHandler(logHandler)
logger.addHandler(fileHandler)
logger.setLevel(logging.INFO)

app = Flask(__name__)
register_correlation_id(app)
metrics = PrometheusMetrics(app)
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
app.register_blueprint(health_bp)

@app.route("/test-sync", methods=["GET"])
def test_sync():
    import time
    start = time.time()
    result = slow_operation("sync test")
    elapsed = (time.time() - start) * 1000
    return jsonify({"result": result, "blocked_for_ms": elapsed})

with app.app_context():
    db.create_all()


@app.route("/test-async", methods=["GET"])
def test_async():
    import time
    start = time.time()
    job = task_queue.enqueue(slow_operation, "async test")
    elapsed = (time.time() - start) * 1000
    return jsonify({"job_id": job.id, "enqueued_in_ms": elapsed})


@app.route("/orders/<int:order_id>/invoice", methods=["POST"])
def request_invoice(order_id):
    data = request.get_json() or {}
    email = data.get("email", "customer@example.com")

    job = task_queue.enqueue(
        generate_invoice, order_id, email,
        retry=Retry(max=3, interval=[2, 5, 10])
    )
    logger.info("Invoice generation enqueued", extra={"order_id": order_id, "job_id": job.id})

    return jsonify({"message": "Invoice generation started", "job_id": job.id}), 202

@app.route("/test-dlq", methods=["GET"])
def test_dlq():
    from tasks import flaky_invoice
    job = task_queue.enqueue(flaky_invoice, 999, retry=Retry(max=2, interval=[1, 2]))
    return jsonify({"job_id": job.id, "message": "This job will fail and retry, then go to DLQ"}), 202



@app.errorhandler(404)
def not_found(e):
    logger.warning("404 Not Found", extra={"path": str(e)})
    return jsonify({"error": "Resource not found"}), 404


@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    socketio.run(
        app, port=3000, debug=False, use_reloader=False, allow_unsafe_werkzeug=True
    )
