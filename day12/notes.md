# Day 12: Asynchronous Messaging & Task Queues

## What I did
- Set up RQ (Redis Queue) using the existing Redis (Memurai) connection from Day 11
- Built a Producer: /auth/register now enqueues a simulated "welcome email" job instead of running it inline
- Built a Consumer: a separate worker.py script that connects to the same Redis queue and processes jobs independently from the Flask app
- Used RQ's SimpleWorker instead of the default Worker, since the default relies on os.fork() which doesn't exist on Windows
- Configured automatic retries (max 3 attempts) using RQ's Retry class for jobs that fail
- Verified failed jobs (after exhausting retries) are captured in RQ's Failed Job Registry, acting as a Dead-Letter Queue so failed jobs aren't silently lost
- Fixed a 2-second connection delay caused by using "localhost" (which triggered an IPv6-then-IPv4 fallback on Windows) by switching to the literal IP 127.0.0.1
- Measured and compared registration response time with vs without the queue, to demonstrate the actual performance benefit

## What I learned
- Producer/Consumer architecture separates "requesting work" from "doing work" - the API responds immediately while a separate worker process handles slow tasks in the background
- RQ's default Worker uses os.fork(), which is Unix-only; SimpleWorker is the Windows-compatible alternative that runs jobs in the same process instead of forking
- RQ's delayed retry scheduling (with_scheduler) also relies on multiprocessing behavior that doesn't work cleanly on Windows; immediate retries (interval=0) are a practical workaround in a Windows dev environment, though real delayed backoff would work as expected on a Linux deployment
- A Dead-Letter Queue's purpose is to make sure a permanently failing job is captured and visible, not silently discarded
- "localhost" can be slower than "127.0.0.1" on Windows due to IPv6 resolution attempts timing out before falling back to IPv4 - worth checking when unexplained delays show up in local network calls
- Bcrypt's hashing time is intentionally slow as a security feature, and shouldn't be mistaken for a performance bug when benchmarking a route

## Testing performed
- Registered a user and confirmed the API responded quickly while the worker terminal showed the "email" task still processing 3 seconds later, proving async decoupling
- Temporarily forced job failures to confirm automatic retries occur (up to 3 attempts) without manual intervention
- Verified failed jobs appear in RQ's FailedJobRegistry (Dead-Letter Queue) via a check script, confirming failure data isn't lost
- Measured and compared response times with the task queue enabled vs. disabled (direct/blocking call), confirming the queue keeps the API responsive
- Restored the failure simulation rate to a low value (20%) and confirmed the app runs cleanly after removing all temporary debug/timing code