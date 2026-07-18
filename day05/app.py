import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

app = Flask(__name__)
basedir = os.path.dirname(os.path.abspath(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(basedir, 'users.db')}"
db = SQLAlchemy(app)

# ---- Global Error Handling Middleware ----
@app.errorhandler(400)
def bad_request(e):
    return jsonify({"success": False, "error": "Bad request - check your input"}), 400

@app.errorhandler(404)
def not_found(e):
    return jsonify({"success": False, "error": "Resource not found"}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"success": False, "error": "Internal server error"}), 500

@app.errorhandler(Exception)
def handle_unexpected_error(e):
    return jsonify({"success": False, "error": str(e)}), 500

# ---- Define the User model (this becomes a real table) ----
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "created_at": self.created_at.isoformat()
        }

#create  
@app.route("/users", methods=["POST"])
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

#Read
@app.route("/users", methods=["GET"])
def get_all_users():
    all_users = User.query.all()
    return jsonify({"success": True, "data": [user.to_dict() for user in all_users]})


@app.route("/users/<int:id>", methods=["GET"])
def get_single_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"success": False, "error": "User not found"}), 404
    return jsonify({"success": True, "data": user.to_dict()})

#update
@app.route("/users/<int:id>", methods=["PUT"])
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

#delete
@app.route("/users/<int:id>", methods=["DELETE"])
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"success": False, "error": "User not found"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"success": True, "message": f"User {id} deleted"})

if __name__ == "__main__":
    app.run(port=3000, debug=True)