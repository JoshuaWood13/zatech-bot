"""invite settings

Revision ID: 0003_invite_settings
Revises: 0002_channel_rules
Create Date: 2025-09-13 00:12:00

"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "0003_invite_settings"
down_revision = "0002_channel_rules"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "invite_settings",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("admin_channel_id", sa.String(length=32), nullable=True),
        sa.Column("notify_on_join", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("dm_message", sa.Text(), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    op.drop_table("invite_settings")

