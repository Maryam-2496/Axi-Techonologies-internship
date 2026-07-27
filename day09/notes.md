# Day 9: Input Validation & Security Hardening

## What I did
- Added schema-based request validation using Marshmallow (RegisterSchema, LoginSchema)
- Built a reusable `@validate_schema` decorator to validate JSON bodies before they reach route logic
- Confirmed SQL Injection protection is already handled by Flask-SQLAlchemy's parameterized queries
- Added XSS input sanitization using `bleach` to strip HTML/script tags from user-submitted text (e.g. name field)
- Noted NoSQL injection prevention is not applicable to SQLite/SQLAlchemy, and is additionally covered by schema validation rejecting non-string input
- Added HTTP security headers using Flask-Talisman (X-Content-Type-Options, X-Frame-Options, CSP)
- Added rate limiting on the login route using Flask-Limiter (10 requests per minute)
- Fixed a circular import bug between app.py and auth_routes.py by moving the limiter into a separate extensions.py file

## What I learned
- Validation should happen before business logic runs, so bad data never reaches the database
- ORMs like SQLAlchemy prevent SQL injection by default as long as you never build raw SQL strings manually
- Sanitizing input isn't just about removing tags — an empty result after sanitization should still be caught by required-field checks
- Circular imports in Flask can silently create duplicate app instances; the fix is to keep shared objects (like a limiter) in their own neutral file
- Rate limiting should be layered with other checks (like validation) but should run first so abusive requests get blocked fastest

## Testing performed
- Sent invalid email/short password to /auth/register → confirmed 400 with clear field errors
- Sent `<b>Ali</b>` as name → confirmed tags stripped, stored as plain text
- Sent 11+ rapid requests to /auth/login → confirmed 11th request returned 429 Too Many Requests
- Sent SQL injection-style payloads (`' OR '1'='1`) as login credentials → confirmed rejected via validation/auth check, never a successful login or crash
- Sent `<img src=x onerror=alert(1)>` as name → confirmed sanitization stripped it to empty, then required-field check caught it with 400