from __future__ import annotations

from typing import Optional
from datetime import datetime, timezone
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncEngine

from ...storage.models import InviteSettings


class InviteSettingsRepository:
    def __init__(self, engine: AsyncEngine) -> None:
        self.engine = engine

    async def get(self) -> Optional[InviteSettings]:
        async with self.engine.connect() as conn:
            res = await conn.execute(select(InviteSettings).limit(1))
            return res.scalar_one_or_none()

    async def upsert(self, *, admin_channel_id: Optional[str] = None, audit_channel_id: Optional[str] = None, notify_on_join: Optional[bool] = None, dm_message: Optional[str] = None) -> None:
        async with self.engine.begin() as conn:
            existing = (await conn.execute(select(InviteSettings).limit(1))).scalar_one_or_none()
            if existing is None:
                await conn.execute(
                    insert(InviteSettings).values(
                        admin_channel_id=admin_channel_id,
                        audit_channel_id=audit_channel_id,
                        notify_on_join=notify_on_join if notify_on_join is not None else True,
                        dm_message=dm_message or "Welcome to the community! Please read the rules in #rules.",
                        updated_at=datetime.now(timezone.utc),
                    )
                )
                return
            values = {"updated_at": datetime.now(timezone.utc)}
            if admin_channel_id is not None:
                values["admin_channel_id"] = admin_channel_id
            if audit_channel_id is not None:
                values["audit_channel_id"] = audit_channel_id
            if notify_on_join is not None:
                values["notify_on_join"] = notify_on_join
            if dm_message is not None:
                values["dm_message"] = dm_message
            await conn.execute(update(InviteSettings).where(InviteSettings.id == existing.id).values(**values))
