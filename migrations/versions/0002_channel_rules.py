"""channel rules

Revision ID: 0002_channel_rules
Revises: 0001_initial
Create Date: 2025-09-13 00:05:00

"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "0002_channel_rules"
down_revision = "0001_initial"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "channel_rules",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("channel_id", sa.String(length=32), nullable=False, unique=True),
        sa.Column("allow_top_level_posts", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("allow_thread_replies", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("allow_bots", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_channel_rules_channel_id", "channel_rules", ["channel_id"], unique=True)


def downgrade() -> None:
    op.drop_index("ix_channel_rules_channel_id", table_name="channel_rules")
    op.drop_table("channel_rules")

