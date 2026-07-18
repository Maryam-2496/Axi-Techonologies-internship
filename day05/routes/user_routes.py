from flask import Blueprint, request, jsonify
from models.user_model import db, User

user_bp = Blueprint("users", __name__)

@user_bp.route("/users", methods=["POST"])
def create_user():
    data = request.json
    if not data or not data.get("name") or not data.get("email"):
        return jsonify({"success": False, "error": "Name and email are required"}), 400

    existing = User.query.filter_by(email=data.get("email")).first()
    if existing:
        return jsonify({"success": False, "error": "Email already exists"}), 400

    new_user = User(name=data.get("name"), email=data.get("email"))
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"success": True, "data": new_user.to_dict()}), 201

@user_bp.route("/users", methods=["GET"])
def get_all_users():
    all_users = User.query.all()
    return jsonify({"success": True, "data": [user.to_dict() for user in all_users]})

@user_bp.route("/users/<int:id>", methods=["GET"])
def get_single_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"success": False, "error": "User not found"}), 404
    return jsonify({"success": True, "data": user.to_dict()})

@user_bp.route("/users/<int:id>", methods=["PUT"])
def update_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"success": False, "error": "User not found"}), 404
    data = request.json
    if not data:
        return jsonify({"success": False, "error": "No data provided"}), 400
    user.name = data.get("name", user.name)
    user.email = data.get("email", user.email)
    db.session.commit()
    return jsonify({"success": True, "data": user.to_dict()})

@user_bp.route("/users/<int:id>", methods=["DELETE"])
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"success": False, "error": "User not found"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"success": True, "message": f"User {id} deleted"})