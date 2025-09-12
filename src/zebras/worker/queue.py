from __future__ import annotations

from typing import Any, Callable
from rq import Queue, Worker
from redis import Redis


def create_queue(redis_conn: Redis, name: str = "zebras") -> Queue:
    return Queue(name, connection=redis_conn)


def start_worker(redis_conn: Redis, name: str = "zebras") -> None:
    q = Queue(name, connection=redis_conn)
    worker = Worker([q])
    worker.work(with_scheduler=True)

