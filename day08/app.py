from flask import Flask
from flask_migrate import Migrate
from models.user import db, User
from models.post import Post
from routes.post_routes import post_bp
import os
from routes.post_routes import post_bp
# ...after app = Flask(__name__) and db.init_app(app)...
app.register_blueprint(post_bp)

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(basedir, 'day08.db')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(post_bp)

if __name__ == "__main__":
    app.run(port=3000, debug=True)