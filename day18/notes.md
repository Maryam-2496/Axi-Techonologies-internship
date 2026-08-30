# Day 18: API Security & System Hardening

## What I did
- Audited SQL/NoSQL injection safeguards -- confirmed all queries already use SQLAlchemy
  ORM (parameterized), no raw string-concatenated SQL anywhere in the project
- Audited XSS & payload sanitization -- confirmed clean_text() and Marshmallow schemas
  (RegisterSchema, LoginSchema) were already in place since Day 9
- Added CORS via flask-cors, restricting allowed origins
- Migrated rate limiting from in-memory storage to Redis-backed moving-window strategy
  (storage_uri="redis://127.0.0.1:6379"), fixing the in-memory storage warning seen
  since Day 9
- Verified the Redis-backed limiter: sent 11+ rapid POST /auth/login requests, confirmed
  10 succeeded and the 11th onward returned 429 Too Many Requests, with flask-limiter's
  log confirming "ratelimit 10 per 1 minute exceeded"
- Added a dedicated 429 error handler so rate-limit responses return JSON instead of
  Flask-Limiter's default HTML page
- Added MAX_CONTENT_LENGTH (10MB) and a 413 error handler for oversized payloads
- Audited full git history for hardcoded secrets (git log --all -p) -- confirmed clean,
  no real JWT_SECRET or other secrets were ever committed; .env.example confirmed to
  only contain placeholder values
- Added a secret-scan job (TruffleHog) to the GitHub Actions CI pipeline, running
  alongside test/build-and-push/deploy -- confirmed passing on the Day 18 PR
- Ran pip-audit -- found 7 known CVEs, all in the pip package itself (v24.2), with
  fixes available in v26.0+; resolved by upgrading pip
- PR merged into main (checks: secret-scan, test, build-and-push passed; deploy still
  fails/skips as expected, no live server provisioned)

## What I learned
- Several of this day's roadmap items were already solved in earlier days (SQL/XSS
  safeguards on Day 9) -- auditing and confirming existing protections still hold is
  as valid a security practice as building something new
- In-memory rate limiting doesn't share state across multiple server instances or
  survive restarts; Redis-backed storage fixes both
- Automated secret scanning in CI catches leaks before they can be merged, rather than
  relying on manual review alone