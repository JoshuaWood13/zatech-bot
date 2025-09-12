"""auto responder rules

Revision ID: 0005_auto_responder_rules
Revises: 0004_invite_audit_channel
Create Date: 2025-09-13 00:40:00

"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "0005_auto_responder_rules"
down_revision = "0004_invite_audit_channel"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "auto_responder_rules",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("phrase", sa.Text(), nullable=False),
        sa.Column("response_text", sa.Text(), nullable=False),
        sa.Column("match_type", sa.String(length=16), nullable=False),
        sa.Column("case_sensitive", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("channel_id", sa.String(length=32), nullable=True),
        sa.Column("enabled", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_auto_responder_rules_channel_id", "auto_responder_rules", ["channel_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_auto_responder_rules_channel_id", table_name="auto_responder_rules")
    op.drop_table("auto_responder_rules")

