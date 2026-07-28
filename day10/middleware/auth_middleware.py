import os
import jwt
from functools import wraps
from flask import request, jsonify

def authenticate_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "No token provided"}), 401

        token = auth_header.split(" ")[1]

        try:
            decoded = jwt.decode(token, os.environ.get("JWT_SECRET"), algorithms=["HS256"])
            request.user = decoded
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 403
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 403

        return f(*args, **kwargs)
    return decorated