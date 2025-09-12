**Persistence & Migrations**

Database
- Default: Postgres via SQLAlchemy 2.x async with asyncpg.
- Configured by `DATABASE_URL` (Neon DSN supported as-is).

Models (initial)
- `event_logs`
  - Columns: id, created_at (tz), event_type, subtype, team_id, channel_id, user_id, message_ts, thread_ts, action, raw (JSONB)
  - Indexes on event_type, team_id, channel_id, user_id
  - Purpose: store normalized metadata and the full raw Slack payload

Migrations
- Tooling: Alembic (configured in `alembic.ini`, scripts in `migrations/`).
- Apply: `zebras db upgrade`
- Roll back: `zebras db downgrade base`

Notes
- Additional tables will be added for rules and audits.
- For local dev, you can use a Dockerized Postgres or Neon.

