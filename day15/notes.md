# Day 15: Observability, Logging & Week 3 Capstone

## What I did
- Structured JSON logging via python-json-logger (adapted from roadmap's Winston/Zap,
  which are Node-only)
- Correlation ID middleware: unique ID per request, attached to every log line via
  logging.setLogRecordFactory + Flask's `g` (the %-style logging.Filter approach didn't
  reliably inject the value, had to switch methods)
- Rotating file logs via concurrent-log-handler (1MB max, 5 backups) to prevent disk
  exhaustion; app.log added to .gitignore
- /healthz (liveness) and /readyz (readiness -- pings SQLite + Redis) endpoints
- Prometheus /metrics endpoint via prometheus-flask-exporter
- Week 3 capstone: pushed day15 as a feature branch, opened PR, merged after CI passed
  (test + build-and-push passed, deploy still skips -- no live server)
- Load tested with Locust: 10 concurrent users, 43 requests, 0 failures
- Confirmed correlation IDs stayed unique per request even under concurrent load
- Simulated a crash (closed the running server mid-traffic) and restart -- confirmed
  Locust's failure count recovered to 0 once the app came back up

## What I learned
- Werkzeug's own internal access-log lines don't reliably get correlation IDs (logged
  outside full request context) -- only app-level logs (routes.auth_routes etc.) do,
  and that's fine/expected
- Rate limiting (429s) under load testing is a good sign, not a bug