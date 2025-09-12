from __future__ import annotations

from typing import Optional
from datetime import datetime, timezone
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncEngine

from ..storage.models import ChannelRule


class ChannelRuleRepository:
    def __init__(self, engine: AsyncEngine) -> None:
        self.engine = engine

    async def get(self, channel_id: str) -> Optional[ChannelRule]:
        async with self.engine.connect() as conn:
            res = await conn.execute(select(ChannelRule).where(ChannelRule.channel_id == channel_id))
            return res.scalar_one_or_none()

    async def upsert(self, channel_id: str,
                     *,
                     allow_top_level_posts: Optional[bool] = None,
                     allow_thread_replies: Optional[bool] = None,
                     allow_bots: Optional[bool] = None) -> None:
        async with self.engine.begin() as conn:
            existing = (await conn.execute(select(ChannelRule).where(ChannelRule.channel_id == channel_id))).scalar_one_or_none()
            if existing is None:
                await conn.execute(
                    insert(ChannelRule).values(
                        channel_id=channel_id,
                        allow_top_level_posts=allow_top_level_posts if allow_top_level_posts is not None else True,
                        allow_thread_replies=allow_thread_replies if allow_thread_replies is not None else True,
                        allow_bots=allow_bots if allow_bots is not None else True,
                        updated_at=datetime.now(timezone.utc),
                    )
                )
                return
            values = {
                "updated_at": datetime.now(timezone.utc),
            }
            if allow_top_level_posts is not None:
                values["allow_top_level_posts"] = allow_top_level_posts
            if allow_thread_replies is not None:
                values["allow_thread_replies"] = allow_thread_replies
            if allow_bots is not None:
                values["allow_bots"] = allow_bots
            if values:
                await conn.execute(update(ChannelRule).where(ChannelRule.channel_id == channel_id).values(**values))

