import os
from redis import Redis
from rq import Queue
from rq.worker import SimpleWorker
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

redis_conn = Redis(host="localhost", port=6379)
queue = Queue(connection=redis_conn)

if __name__ == "__main__":
    worker = SimpleWorker([queue], connection=redis_conn)
worker.work()
