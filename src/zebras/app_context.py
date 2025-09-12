from __future__ import annotations

from dataclasses import dataclass
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncEngine
from redis import Redis


@dataclass
class AppContext:
    engine: AsyncEngine
    redis: Redis


ctx: Optional[AppContext] = None


def set_context(context: AppContext) -> None:
    global ctx
    ctx = context


def get_context() -> AppContext:
    if ctx is None:
        raise RuntimeError("App context not initialized")
    return ctx

