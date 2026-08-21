from extensions import redis_client
from rq import Queue
from tasks import slow_operation
import time

q = Queue(connection=redis_client)
start = time.time()
for i in range(1000):
    q.enqueue(slow_operation, f"job-{i}")
elapsed = time.time() - start
print(f"Enqueued 1000 jobs in {elapsed:.2f}s")