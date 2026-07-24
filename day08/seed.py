from app import app, db
from models.user import User

with app.app_context():
    if not User.query.filter_by(username="ali_test").first():
        user = User(
            username="ali_test",
            email="ali@example.com",
            password_hash="dummyhash123"
        )
        db.session.add(user)
        db.session.commit()
        print("Test user created:", user.id, user.username)
    else:
        print("Test user already exists")