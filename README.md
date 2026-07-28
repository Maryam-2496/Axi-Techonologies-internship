# AXI Internship

6-week backend engineering and Ai internship progress log.

## Structure
Each `dayXX/` folder contains that day's `app.py`, notes, and screenshots.

## Progress
- Day 1 — Backend Fundamentals: basic Flask server on port 3000.
- Day 2 — REST APIs & Routing: query/path parameters, POST endpoint returning 201 Created.
- Day 3 — In-Memory Database & CRUD Operations: implemented a temporary users database, auto-increment IDs, CRUD (Create, Read, Update, Delete) APIs, and tested endpoints using Postman.
- Day 4 — Real Database (SQLite + SQLAlchemy): schema, migrations, full CRUD against disk-backed storage, verified persistence across restarts.
- Day 5 — Production Readiness: global error handling, modular architecture, linting, edge-case testing, and PR workflow practice. Week 1 complete!
- Day 6 – Authentication & Password Security: added password_hash to the User model, hashed passwords with bcrypt on registration, built /auth/register and /auth/login with generic 401 errors, and implemented JWT generation (1-hour expiry) on successful login.
- Day 7 – Protecting Endpoints with Auth Middleware: built authenticateToken middleware to verify JWT signatures from the Authorization header, protected GET/PUT/DELETE /auth/me with it, and tested the full matrix — valid token, missing token (401), invalid/expired token (403), and deleted-user-with-valid-token (404).
- Day 8 — Relational Database Modeling & Foreign Keys: designed a One-to-Many relationship between User and Post models, implemented foreign key constraints, performed database migrations, queried related records using SQLAlchemy ORM, and built user-specific API endpoints.
- Day 9 – Input Validation & Security Hardening: implemented request validation using Marshmallow, added XSS input sanitization, confirmed SQL injection protection via SQLAlchemy's parameterized queries, added security headers with Flask-Talisman, and configured rate limiting on the login route with Flask-Limiter.
- Day 10 – Code Refactoring, Comprehensive Testing & Review: reviewed layered architecture, added centralized error handling for 404/500, regenerated requirements.txt, and audited .env files across all days for secrets. Built a PyTest suite with 7 automated tests covering registration, login, XSS sanitization, and rate limiting. Added Swagger/OpenAPI documentation via Flasgger, resolving a Content-Security-Policy conflict between Flask-Talisman and Swagger UI. Week 2 complete!