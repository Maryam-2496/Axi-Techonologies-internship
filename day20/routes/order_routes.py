import json
import logging
from flask import Blueprint, request, jsonify
from middleware.auth_middleware import authenticate_token
from models.order_model import db, Order
from extensions import redis_client, task_queue
from tasks import send_order_summary_email

order_bp = Blueprint("orders", __name__)
logger = logging.getLogger(__name__)


@order_bp.route("/orders", methods=["POST"])
@authenticate_token
def create_order():
    data = request.get_json() or {}
    item_name = data.get("item_name")
    amount = data.get("amount")

    if not item_name or amount is None:
        return jsonify({"error": "item_name and amount are required"}), 400

    order = Order(user_id=request.user["userId"], item_name=item_name, amount=amount)
    db.session.add(order)
    db.session.commit()

    redis_client.delete(f"orders:{request.user['userId']}")

    job = task_queue.enqueue(send_order_summary_email, request.user["userId"], order.id)
    logger.info("Order created", extra={"order_id": order.id, "job_id": job.id})

    return jsonify(order.to_dict()), 201


@order_bp.route("/orders", methods=["GET"])
@authenticate_token
def get_my_orders():
    cache_key = f"orders:{request.user['userId']}"

    cached = redis_client.get(cache_key)
    if cached:
        return jsonify({"source": "cache", "orders": json.loads(cached)}), 200

    orders = Order.query.filter_by(user_id=request.user["userId"]).all()
    result = [o.to_dict() for o in orders]

    redis_client.set(cache_key, json.dumps(result), ex=300)

    return jsonify({"source": "database", "orders": result}), 200