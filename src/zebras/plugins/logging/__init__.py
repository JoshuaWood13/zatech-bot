from __future__ import annotations

import logging
from typing import Any, Dict

from ...plugin import Registry
from ...app_context import get_context
from ...storage.repositories import EventLogRepository


def register(reg: Registry) -> None:
    log = logging.getLogger("zebras.plugins.logging")

    async def _persist(event_type: str, payload: Dict[str, Any]) -> None:
        ctx = get_context()
        repo = EventLogRepository(ctx.engine)
        e = payload.get("event", payload)
        await repo.log(
            event_type=event_type,
            raw=payload,
            subtype=e.get("subtype"),
            team_id=payload.get("team_id") or e.get("team"),
            channel_id=(e.get("channel") if isinstance(e.get("channel"), str) else (e.get("channel", {}) or {}).get("id")),
            user_id=e.get("user"),
            message_ts=e.get("ts"),
            thread_ts=e.get("thread_ts"),
        )

    @reg.events.on("message")
    async def on_message(event: Dict[str, Any]) -> None:
        e = event.get("event", event)
        log.info("message", extra={"user": e.get("user"), "channel": e.get("channel"), "subtype": e.get("subtype")})
        await _persist("message", event)

    @reg.events.on("channel_created")
    async def on_channel_created(event: Dict[str, Any]) -> None:
        e = event.get("event", event)
        log.info("channel_created", extra={"channel": e.get("channel")})
        await _persist("channel_created", event)

    @reg.events.on("channel_rename")
    async def on_channel_rename(event: Dict[str, Any]) -> None:
        e = event.get("event", event)
        log.info("channel_rename", extra={"channel": e.get("channel")})
        await _persist("channel_rename", event)

    @reg.events.on("channel_deleted")
    async def on_channel_deleted(event: Dict[str, Any]) -> None:
        e = event.get("event", event)
        log.info("channel_deleted", extra={"channel": e.get("channel")})
        await _persist("channel_deleted", event)

    @reg.events.on("channel_archive")
    async def on_channel_archive(event: Dict[str, Any]) -> None:
        e = event.get("event", event)
        log.info("channel_archive", extra={"channel": e.get("channel")})
        await _persist("channel_archive", event)

    @reg.events.on("channel_unarchive")
    async def on_channel_unarchive(event: Dict[str, Any]) -> None:
        e = event.get("event", event)
        log.info("channel_unarchive", extra={"channel": e.get("channel")})
        await _persist("channel_unarchive", event)

    @reg.events.on("team_join")
    async def on_team_join(event: Dict[str, Any]) -> None:
        e = event.get("event", event)
        log.info("team_join", extra={"user": e.get("user")})
        await _persist("team_join", event)

    @reg.events.on("user_change")
    async def on_user_change(event: Dict[str, Any]) -> None:
        e = event.get("event", event)
        log.info("user_change", extra={"user": e.get("user")})
        await _persist("user_change", event)
