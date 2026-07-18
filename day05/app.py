import os
from flask import Flask, jsonify
from dotenv import load_dotenv
from models.user_model import db
from routes.user_routes import user_bp

basedir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(basedir, ".env"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(basedir, 'users.db')}"
db.init_app(app)

app.register_blueprint(user_bp)


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


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(port=3000, debug=True)
