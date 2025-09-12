from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, Optional

from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncEngine

from .models import EventLog


class EventLogRepository:
    def __init__(self, engine: AsyncEngine) -> None:
        self.engine = engine

    async def log(self, *,
                  event_type: str,
                  raw: Dict[str, Any],
                  subtype: Optional[str] = None,
                  team_id: Optional[str] = None,
                  channel_id: Optional[str] = None,
                  user_id: Optional[str] = None,
                  message_ts: Optional[str] = None,
                  thread_ts: Optional[str] = None,
                  action: Optional[str] = None) -> None:
        now = datetime.now(timezone.utc)
        stmt = insert(EventLog).values(
            created_at=now,
            event_type=event_type,
            subtype=subtype,
            team_id=team_id,
            channel_id=channel_id,
            user_id=user_id,
            message_ts=message_ts,
            thread_ts=thread_ts,
            action=action,
            raw=raw,
        )
        async with self.engine.begin() as conn:
            await conn.execute(stmt)

