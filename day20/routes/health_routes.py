import logging
from flask import Blueprint, jsonify
from sqlalchemy import text
from models.user_model import db
from extensions import redis_client

health_bp = Blueprint("health", __name__)
logger = logging.getLogger(__name__)


@health_bp.route("/healthz", methods=["GET"])
def healthz():
    """Basic liveness check — is the app process running at all."""
    return jsonify({"status": "ok"}), 200


@health_bp.route("/readyz", methods=["GET"])
def readyz():
    """Readiness check — can the app actually serve traffic (DB + Redis reachable)."""
    checks = {}
    healthy = True

    try:
        db.session.execute(text("SELECT 1"))
        checks["database"] = "ok"
    except Exception as e:
        checks["database"] = "unreachable"
        healthy = False
        logger.error("Readiness check failed: database", extra={"error": str(e)})

    try:
        redis_client.ping()
        checks["redis"] = "ok"
    except Exception as e:
        checks["redis"] = "unreachable"
        healthy = False
        logger.error("Readiness check failed: redis", extra={"error": str(e)})

    status_code = 200 if healthy else 503
    return jsonify({"status": "ok" if healthy else "degraded", "checks": checks}), status_code