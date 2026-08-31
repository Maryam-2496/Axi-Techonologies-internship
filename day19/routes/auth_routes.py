import os
import jwt
import logging
from datetime import datetime, timedelta, timezone
from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from models.user_model import db, User
from middleware.auth_middleware import authenticate_token
from schemas import RegisterSchema, LoginSchema
from validation import validate_schema
from sanitize import clean_text
import json
from extensions import limiter, redis_client, task_queue
from tasks import send_welcome_email
from rq import Retry
from events import publish_event

auth_bp = Blueprint("auth", __name__)
bcrypt = Bcrypt()
logger = logging.getLogger(__name__)


@auth_bp.route("/auth/register", methods=["POST"])
@validate_schema(RegisterSchema)
def register():
    """
    Register a new user
    ---
    tags:
      - Auth
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              example: Ali Khan
            email:
              type: string
              example: ali@example.com
            password:
              type: string
              example: password123
    responses:
      201:
        description: User created successfully
      400:
        description: Validation error or email already registered
    """
    data = request.get_json()
    name = data.get("name")
    name = clean_text(name)
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({"error": "name, email, and password are required"}), 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        logger.warning("Registration failed: email already exists", extra={"email": email})
        return jsonify({"error": "Email already registered"}), 400

    hashed_pw = bcrypt.generate_password_hash(password).decode("utf-8")

    new_user = User(name=name, email=email, password_hash=hashed_pw)
    db.session.add(new_user)
    db.session.commit()
    publish_event("user_registered", {"user_id": new_user.id, "email": new_user.email})
    logger.info("New user registered", extra={"user_id": new_user.id, "email": new_user.email})

    task_queue.enqueue(
        send_welcome_email,
        new_user.email,
        new_user.name,
        retry=Retry(max=3, interval=0),
    )

    return jsonify(new_user.to_dict()), 201


@auth_bp.route("/auth/login", methods=["POST"])
@limiter.limit("10 per minute")
@validate_schema(LoginSchema)
def login():
    """
    Log in an existing user
    ---
    tags:
      - Auth
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
              example: ali@example.com
            password:
              type: string
              example: password123
    responses:
      200:
        description: Login successful, returns JWT token
      401:
        description: Invalid email or password
      429:
        description: Too many login attempts
    """
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "email and password are required"}), 400

    user = User.query.filter_by(email=email).first()

    if not user or not bcrypt.check_password_hash(user.password_hash, password):
        logger.warning("Login failed: invalid credentials", extra={"email": email})
        return jsonify({"error": "Invalid email or password"}), 401

    token_payload = {
        "userId": user.id,
        "email": user.email,
        # "exp": datetime.now(timezone.utc) + timedelta(seconds=5),
        "exp": datetime.now(timezone.utc) + timedelta(hours=1),
    }
    token = jwt.encode(token_payload, os.environ.get("JWT_SECRET"), algorithm="HS256")

    logger.info("User logged in", extra={"user_id": user.id})
    return jsonify({"token": token, "user": user.to_dict()}), 200


@auth_bp.route("/auth/me", methods=["GET"])
@authenticate_token
def get_current_user():
    cache_key = f"user:{request.user['userId']}"

    cached_user = redis_client.get(cache_key)
    if cached_user:
        return jsonify(json.loads(cached_user)), 200

    user = User.query.get(request.user["userId"])

    if not user:
        return jsonify({"error": "User not found"}), 404

    user_data = user.to_dict()
    redis_client.set(cache_key, json.dumps(user_data), ex=300)

    return jsonify(user_data), 200


@auth_bp.route("/auth/me", methods=["PUT"])
@authenticate_token
def update_current_user():
    user = User.query.get(request.user["userId"])

    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    name = data.get("name")

    if name:
        user.name = name
        db.session.commit()
        redis_client.delete(f"user:{user.id}")

    return jsonify(user.to_dict()), 200


@auth_bp.route("/auth/me", methods=["DELETE"])
@authenticate_token
def delete_current_user():
    user = User.query.get(request.user["userId"])

    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    redis_client.delete(f"user:{user.id}")
    logger.info("Account deleted", extra={"user_id": user.id})

    return jsonify({"message": "Account deleted"}), 200