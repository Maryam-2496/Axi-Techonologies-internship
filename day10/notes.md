# Day 10: Code Refactoring, Comprehensive Testing & Review

## What I did
- Copied Day 9's working code into a fresh day10 folder to safely refactor without risking the tested Day 9 checkpoint
- Reviewed layered architecture (routes/models/middleware/schemas) — confirmed structure is clean for this project's size
- Added centralized error handlers for 404 and 500, so unexpected errors return clean JSON instead of raw tracebacks
- Regenerated requirements.txt properly using pip freeze (previously empty by mistake)
- Audited .env / .env.example across day08, day09, day10 to confirm secrets stay out of git
- Set up PyTest with an in-memory test database fixture, isolated from real data
- Wrote 7 automated tests covering register success/failure, duplicate email, login success/failure, XSS sanitization, and rate limiting
- Added Swagger/OpenAPI documentation using Flasgger, with docstrings for /auth/register and /auth/login
- Fixed a Content-Security-Policy conflict between Flask-Talisman and Swagger UI by explicitly allowing Swagger's known script/style/font sources

## What I learned
- Copying a day's code into a new folder before refactoring protects the last known-good checkpoint
- Automated tests catch regressions instantly (e.g. the rate-limit test reproduces what used to be a manual multi-request Thunder Client test)
- An in-memory SQLite database for testing keeps test data completely separate from real user data
- Security headers (CSP) can conflict with legitimate tools like Swagger UI — the fix is an explicit allow-list, not disabling the protection
- Swagger docs are generated directly from route docstrings, so documentation stays close to the actual code

## Testing performed
- Ran full PyTest suite (7 tests) — all passed
- Verified Swagger UI loads at /apidocs and lists both /auth/register and /auth/login with example request bodies
- Verified .env is git-ignored and .env.example is trackable in day10