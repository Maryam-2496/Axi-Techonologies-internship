from flask import Blueprint, jsonify, request
from sqlalchemy import text
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import db, User
from models.post import Post

post_bp = Blueprint("post_bp", __name__)

@post_bp.route("/users/<int:user_id>/posts", methods=["GET"])
def get_user_posts(user_id):
    # Eager loading: fetch User AND their related Posts in one go
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    posts_data = [
        {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "created_at": post.created_at.isoformat()
        }
        for post in user.posts  # uses the relationship() from Task 1
    ]

    return jsonify({"user": user.username, "posts": posts_data})


@post_bp.route("/users-posts-join", methods=["GET"])
def get_users_posts_join():
    # Raw SQL INNER JOIN — manually combining users and posts tables
    result = db.session.execute(text("""
        SELECT users.id AS user_id, users.username, posts.id AS post_id, posts.title
        FROM users
        INNER JOIN posts ON users.id = posts.user_id
    """))
    rows = [dict(row._mapping) for row in result]
    return jsonify(rows)


@post_bp.route("/posts", methods=["POST"])
@jwt_required()
def create_post():
    user_id = get_jwt_identity()
    data = request.get_json()
    new_post = Post(title=data["title"], content=data["content"], user_id=user_id)
    db.session.add(new_post)
    db.session.commit()
    return jsonify({"id": new_post.id, "title": new_post.title}), 201