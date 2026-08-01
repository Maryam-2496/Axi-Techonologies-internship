from redis import Redis
from rq import Queue
from rq.registry import FailedJobRegistry

redis_conn = Redis(host="localhost", port=6379)
queue = Queue(connection=redis_conn)
registry = FailedJobRegistry(queue=queue)

failed_job_ids = registry.get_job_ids()
print("Failed job IDs (Dead-Letter Queue):", failed_job_ids)

for job_id in failed_job_ids:
    job = queue.fetch_job(job_id)
    print(f"\nJob {job_id}:")
    print("  Function:", job.func_name)
    print("  Args:", job.args)
    print("  Exception:", job.exc_info.splitlines()[-1] if job.exc_info else "N/A")