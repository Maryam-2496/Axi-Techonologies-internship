from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import redis

limiter = Limiter(get_remote_address, default_limits=[])
redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)