from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import redis
from rq import Queue
from flask_socketio import SocketIO

limiter = Limiter(get_remote_address, default_limits=[])
redis_client = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True)
task_queue = Queue(connection=redis.Redis(host="127.0.0.1", port=6379))
socketio = SocketIO(cors_allowed_origins="*", async_mode="threading")
# socketio = SocketIO(cors_allowed_origins="*", async_mode="threading")
# socketio = SocketIO(cors_allowed_origins="*")
