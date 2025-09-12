"""add audit_channel_id to invite_settings

Revision ID: 0004_invite_audit_channel
Revises: 0003_invite_settings
Create Date: 2025-09-13 00:25:00

"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "0004_invite_audit_channel"
down_revision = "0003_invite_settings"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("invite_settings", sa.Column("audit_channel_id", sa.String(length=32), nullable=True))


def downgrade() -> None:
    op.drop_column("invite_settings", "audit_channel_id")

