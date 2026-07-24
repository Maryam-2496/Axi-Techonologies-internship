from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from models.user import User

auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data.get("username")).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    token = create_access_token(identity=str(user.id))
    return jsonify({"access_token": token})