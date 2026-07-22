# Day 7 — Protecting Endpoints with Auth Middleware

## Task 1: Understanding Headers & Middleware
- Learned how Authorization: Bearer <token> headers work
- Understood middleware as code that runs before a route's actual function, to validate the request first

## Task 2: authenticateToken Middleware
- Built middleware that extracts the token from the Authorization header
- Rejects missing tokens with 401
- Verifies the JWT signature against JWT_SECRET
- Returns 403 for expired or tampered tokens
- Attaches decoded payload to request.user so routes know who's calling

## Task 3: Protected /auth/me Route
- Built GET /auth/me using request.user["userId"] to fetch the current user
- Tested: valid token (200), no token (401), invalid token (403)

## Task 4: Protecting CRUD + Final Verification
- Added PUT /auth/me and DELETE /auth/me, both behind the same middleware
- Confirmed users can only update/delete their own account via the token, never someone else's
- Tested expired tokens by temporarily shortening expiry to 5 seconds, confirmed 403, then reverted back to 1 hour
- Full test matrix: valid token (200), no token (401), invalid token (403), expired token (403), deleted-user-but-valid-token (404)

## Bugs fixed today
- Pasted the /auth/me route in the middle of the login function, breaking login entirely — split back into separate route blocks
- URL typo (/auth/lme instead of /auth/me) caused a false 404 during expired-token testing