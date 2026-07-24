from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    # This is the "One" side of the One-to-Many relationship.
    # It doesn't create a column — it lets us do user.posts to get all their posts.
    posts = db.relationship("Post", backref="author", cascade="all, delete-orphan")
