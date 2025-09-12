from __future__ import annotations

from typing import Optional
import redis


def create_redis(url: str) -> redis.Redis:
    return redis.from_url(url)

