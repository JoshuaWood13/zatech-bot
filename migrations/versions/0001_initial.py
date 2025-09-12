"""initial tables

Revision ID: 0001_initial
Revises: 
Create Date: 2025-09-12 00:00:00

"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "event_logs",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("event_type", sa.String(length=64), nullable=False),
        sa.Column("subtype", sa.String(length=64), nullable=True),
        sa.Column("team_id", sa.String(length=32), nullable=True),
        sa.Column("channel_id", sa.String(length=32), nullable=True),
        sa.Column("user_id", sa.String(length=32), nullable=True),
        sa.Column("message_ts", sa.String(length=32), nullable=True),
        sa.Column("thread_ts", sa.String(length=32), nullable=True),
        sa.Column("action", sa.String(length=64), nullable=True),
        sa.Column("raw", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
    )
    op.create_index("ix_event_logs_event_type", "event_logs", ["event_type"], unique=False)
    op.create_index("ix_event_logs_team_id", "event_logs", ["team_id"], unique=False)
    op.create_index("ix_event_logs_channel_id", "event_logs", ["channel_id"], unique=False)
    op.create_index("ix_event_logs_user_id", "event_logs", ["user_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_event_logs_user_id", table_name="event_logs")
    op.drop_index("ix_event_logs_channel_id", table_name="event_logs")
    op.drop_index("ix_event_logs_team_id", table_name="event_logs")
    op.drop_index("ix_event_logs_event_type", table_name="event_logs")
    op.drop_table("event_logs")

