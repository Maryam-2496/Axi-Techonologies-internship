# Day 17: Asynchronous Processing & Task Queues

## What I did
(Adapted from roadmap's RabbitMQ/Celery/BullMQ to existing stack: Redis + RQ, already
set up since Day 12)
- Proved sync vs async trade-off directly: a 3-second task run inline in a route
  blocked the request for 3.04s; the same task enqueued via RQ returned in 31ms
- Mapped roadmap's broker terms to RQ: Flask route = producer, worker.py = consumer,
  Redis list = queue (no exchanges/routing keys needed in RQ)
- Checked message durability: Memurai has RDB snapshotting on (appendonly: no) --
  jobs are durable on a delay (up to ~60s), not instantly; noted as an acceptable
  trade-off for this exercise, would need appendonly yes for stricter guarantees
- Built /orders/<id>/invoice route to enqueue generate_invoice as a real background
  job producer, returns 202 Accepted with a job_id
- Added exponential backoff retries (Retry(max=3, interval=[2, 5, 10])) to the
  invoice job
- Reused existing DLQ setup from Day 12; tested with a new always-failing task
  (flaky_invoice) to confirm retry-then-fail routing still works
- Added a simple in-memory idempotency check to generate_invoice (skips duplicate
  order_ids) -- noted as demo-only, a real version would check the database instead
- Load tested the queue: enqueued 1000 jobs in 1.75s
- Fault injection: closed the worker process mid-job, restarted it in a new terminal --
  confirmed a new worker instance picked up the remaining queue automatically

## What I learned
- RQ gives at-least-once delivery by default -- a crashed worker doesn't lose the
  queue, but tasks need to be safe to run more than once (idempotency matters)
- HTTP 202 Accepted is the correct status code for "job enqueued, not yet done" --
  not 200