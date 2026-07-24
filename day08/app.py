from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from models.user import db, User
from models.post import Post
import os
from dotenv import load_dotenv

load_dotenv()

# 1. Create app FIRST
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(basedir, 'day08.db')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

# 2. Init extensions
db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

# 3. Import blueprints AFTER app exists, then register
from routes.post_routes import post_bp
from routes.auth_routes import auth_bp
app.register_blueprint(post_bp)
app.register_blueprint(auth_bp)

if __name__ == "__main__":
    app.run(port=3000, debug=True)