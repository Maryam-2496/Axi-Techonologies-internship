from functools import wraps
from flask import request, jsonify


def validate_schema(schema):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            data = request.get_json(silent=True) or {}
            errors = schema().validate(data)
            if errors:
                return jsonify({"errors": errors}), 400
            return f(*args, **kwargs)

        return wrapper

    return decorator
