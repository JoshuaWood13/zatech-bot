from __future__ import annotations

from dataclasses import dataclass
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncEngine
from redis import Redis
from slack_sdk.web.async_client import AsyncWebClient


@dataclass
class AppContext:
    engine: AsyncEngine
    redis: Redis
    bot_token: Optional[str] = None
    _web_client: Optional[AsyncWebClient] = None

    async def web_client(self) -> AsyncWebClient:
        if self._web_client is None:
            if not self.bot_token:
                raise RuntimeError("SLACK_BOT_TOKEN not configured for web client")
            self._web_client = AsyncWebClient(token=self.bot_token)
        return self._web_client


ctx: Optional[AppContext] = None


def set_context(context: AppContext) -> None:
    global ctx
    ctx = context


def get_context() -> AppContext:
    if ctx is None:
        raise RuntimeError("App context not initialized")
    return ctx
