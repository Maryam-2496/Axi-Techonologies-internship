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
    try:
        new_user = User(name=data.get("name"), email=data.get("email"))
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Email already exists or invalid data"}), 400

#Read
@app.route("/users", methods=["GET"])
def get_all_users():
    all_users = User.query.all()
    return jsonify([user.to_dict() for user in all_users])

@app.route("/users/<int:id>", methods=["GET"])
def get_single_user(id):
    user = User.query.get(id)
    if user:
        return jsonify(user.to_dict())
    return jsonify({"error": "User not found"}), 404

#update
@app.route("/users/<int:id>", methods=["PUT"])
def update_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    data = request.json
    user.name = data.get("name", user.name)
    user.email = data.get("email", user.email)
    db.session.commit()
    return jsonify(user.to_dict())

#Delete
@app.route("/users/<int:id>", methods=["DELETE"])
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": f"User {id} deleted"})

if __name__ == "__main__":
    app.run(port=3000, debug=True)