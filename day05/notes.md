# Day 5 Notes

- Added global error handling middleware with standardized {success, error} response format.
- Restructured project into models/ and routes/ using Flask Blueprints for separation of concerns.
- Added .env.example as a safe configuration template; .env itself is now gitignored.
- Linted and auto-formatted code using Black and Flake8.
- Tested edge cases: empty payloads, invalid ID types, duplicate emails, missing fields.
- Practiced the branch → pull request → merge workflow used in real team environments.