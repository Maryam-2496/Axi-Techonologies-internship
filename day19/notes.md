# Day 19: System Design & Architecture Patterns

## What I did
- Documented this project's structure as a modular monolith: routes/, models/,
  middleware/, tasks.py separated by responsibility -- noted how each could be
  extracted into a standalone microservice later without a rewrite
- Compared REST vs async pub/sub communication using the project's own existing
  examples: POST /auth/login (sync REST) vs POST /orders/<id>/invoice (async,
  202 Accepted, processed later via RQ)
- Built a simple event publisher/subscriber using Redis Pub/Sub: publish_event()
  fires a "user_registered" event on registration; a separate subscriber process
  received it in real time, demonstrating decoupled, eventually-consistent
  communication
- Demonstrated an explicit transaction with rollback (add user -> simulated
  failure -> rollback -> confirmed user was never persisted), proving atomicity
- Noted SQLite's simpler isolation model (file-level locking) vs Postgres's
  configurable Read Committed / Repeatable Read / Serializable levels -- flagged
  as a known limitation of the current stack
- Audited existing API gateway-style responsibilities already present in the
  app (centralized JWT auth, Talisman security headers, blueprint-based routing)
  and added a request-normalization hook (trailing slash handling)
- Documented how the existing /healthz and /readyz health checks (Day 15) are a
  direct prerequisite for real service discovery in a multi-service setup
- Diagrammed a high-availability real-time order processing architecture: client
  -> API gateway -> order service -> cache/database/message queue -> background
  workers -> WebSocket push back to client
- Wrote a trade-off defense covering database partitioning (read replica lag),
  caching (invalidation complexity), and async queues (at-least-once delivery,
  idempotency requirement)

## What I learned
- Most of this day's concepts were things the project already does in practice
  (event-driven jobs, health checks, centralized auth) -- system design is often
  about naming and defending patterns you've already built, not just inventing
  new ones
- Every architectural choice has a real cost, not just a benefit -- caching adds
  invalidation complexity, async queues sacrifice immediate consistency, read
  replicas introduce lag