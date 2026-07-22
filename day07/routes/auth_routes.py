import os
import jwt
from datetime import datetime, timedelta, timezone
from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from models.user_model import db, User
from middleware.auth_middleware import authenticate_token

auth_bp = Blueprint("auth", __name__)
bcrypt = Bcrypt()


@auth_bp.route("/auth/register", methods=["POST"])
def register():
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({"error": "name, email, and password are required"}), 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"error": "Email already registered"}), 400

    hashed_pw = bcrypt.generate_password_hash(password).decode("utf-8")

    new_user = User(name=name, email=email, password_hash=hashed_pw)
    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user.to_dict()), 201


@auth_bp.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "email and password are required"}), 400

    user = User.query.filter_by(email=email).first()

    if not user or not bcrypt.check_password_hash(user.password_hash, password):
        return jsonify({"error": "Invalid email or password"}), 401

    token_payload = {
        "userId": user.id,
        "email": user.email,
       # "exp": datetime.now(timezone.utc) + timedelta(seconds=5),
        "exp": datetime.now(timezone.utc) + timedelta(hours=1),
    }
    token = jwt.encode(token_payload, os.environ.get("JWT_SECRET"), algorithm="HS256")

    return jsonify({"token": token, "user": user.to_dict()}), 200


@auth_bp.route("/auth/me", methods=["GET"])
@authenticate_token
def get_current_user():
    user = User.query.get(request.user["userId"])

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify(user.to_dict()), 200

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

    return jsonify(user.to_dict()), 200


@auth_bp.route("/auth/me", methods=["DELETE"])
@authenticate_token
def delete_current_user():
    user = User.query.get(request.user["userId"])

    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "Account deleted"}), 200