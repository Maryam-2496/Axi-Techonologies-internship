# Day 4 Notes

- Learned about statelessness, SQL vs NoSQL, and RAM vs disk storage.
- Installed Flask-SQLAlchemy and python-dotenv, connected via a .env file.
- Defined a User model (id, name, email unique, created_at) using SQLAlchemy.
- Created a real SQLite database (users.db) and generated the table with db.create_all().
- Refactored all CRUD routes (POST, GET all, GET by id, PUT, DELETE) to use real database queries instead of an in-memory list.
- Verified unique email constraint rejects duplicates with a 400 error.
- Restart test: stopped and restarted the server, confirmed data survived — unlike Day 3's in-memory storage.