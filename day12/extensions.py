from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import redis
from rq import Queue

limiter = Limiter(get_remote_address, default_limits=[])
redis_client = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True)
task_queue = Queue(connection=redis.Redis(host="127.0.0.1", port=6379))