from __future__ import annotations

from typing import Any, Awaitable, Callable, Dict, List, Optional
import asyncio
import logging


EventHandler = Callable[[Dict[str, Any]], Awaitable[None]]
Middleware = Callable[[Dict[str, Any], Callable[[Dict[str, Any]], Awaitable[None]]], Awaitable[None]]


class Router:
    """Simple async event router with middleware pipeline."""

    def __init__(self) -> None:
        self._log = logging.getLogger("zebras.router")
        self._handlers: Dict[str, List[EventHandler]] = {}
        self._middleware: List[Middleware] = []

    def add_middleware(self, mw: Middleware) -> None:
        self._middleware.append(mw)

    def on(self, event_type: str, handler: EventHandler) -> None:
        self._handlers.setdefault(event_type, []).append(handler)

    async def dispatch(self, event: Dict[str, Any]) -> None:
        etype = event.get("type") or event.get("event", {}).get("type")
        if not etype:
            self._log.debug("Ignoring event without type: %s", event)
            return

        async def call_handlers(evt: Dict[str, Any]) -> None:
            for h in self._handlers.get(etype, []):
                try:
                    await h(evt)
                except Exception:
                    self._log.exception("Handler error for %s", etype)

        # Compose middleware chain
        handler = call_handlers
        for mw in reversed(self._middleware):
            next_handler = handler

            async def composed(e: Dict[str, Any], mw=mw, nxt=next_handler) -> None:
                await mw(e, nxt)

            handler = composed

        await handler(event)

