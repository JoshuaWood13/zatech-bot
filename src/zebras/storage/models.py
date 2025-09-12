from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import String, Integer, DateTime, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB


class Base(DeclarativeBase):
    pass


class EventLog(Base):
    __tablename__ = "event_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    event_type: Mapped[str] = mapped_column(String(64), index=True)
    subtype: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)

    team_id: Mapped[Optional[str]] = mapped_column(String(32), index=True)
    channel_id: Mapped[Optional[str]] = mapped_column(String(32), index=True)
    user_id: Mapped[Optional[str]] = mapped_column(String(32), index=True)

    message_ts: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    thread_ts: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)

    action: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)

    raw: Mapped[dict] = mapped_column(JSONB)


class ChannelRule(Base):
    __tablename__ = "channel_rules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    channel_id: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    allow_top_level_posts: Mapped[bool] = mapped_column(default=True)
    allow_thread_replies: Mapped[bool] = mapped_column(default=True)
    allow_bots: Mapped[bool] = mapped_column(default=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class InviteSettings(Base):
    __tablename__ = "invite_settings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    admin_channel_id: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    audit_channel_id: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    notify_on_join: Mapped[bool] = mapped_column(default=True)
    dm_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
