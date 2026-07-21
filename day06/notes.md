# Day 6 — Authentication & Password Security

## Task 1: Secure Password Hashing
- Added `password_hash` column to the User model
- Installed flask-bcrypt, hash passwords on registration with bcrypt.generate_password_hash
- Never store or return plaintext passwords

## Task 2: Authentication Endpoints
- Built POST /auth/register — validates input, checks for duplicate email, hashes password
- Built POST /auth/login — verifies password with bcrypt.check_password_hash
- Return one generic "Invalid email or password" message on any auth failure, so we don't leak which emails are registered

## Task 3: JWT Implementation
- Installed PyJWT, added JWT_SECRET to .env (gitignored)
- Login now signs a token containing userId, email, and a 1-hour expiration
- Fixed a bug where load_dotenv() couldn't find .env — needed an explicit path

## Task 4: Verification
- Registered Ali and Sara, confirmed both hash correctly in users.db (SQLite Viewer)
- Tested login: correct password (200 + token), wrong password (401), nonexistent email (401)

## Bugs fixed today
- users.db was defaulting into an /instance/ folder — fixed with an absolute path in app.py
- Login route was accidentally stacked under the register function's decorator — split into its own function
- JWT_SECRET wasn't loading — load_dotenv() needed the .env file's full path