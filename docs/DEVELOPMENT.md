**Development Setup**

Prereqs
- Python 3.11+
- A Slack app created in your workspace (use the manifest below)

Environment
- Copy `.env.example` -> `.env` and set:
  - `SLACK_BOT_TOKEN=xoxb-...`
  - `SLACK_SIGNING_SECRET=...` (HTTP mode)
  - `SLACK_APP_TOKEN=xapp-...` (Socket Mode)

Run (Socket Mode)
- `python -m <package>.run socket` (TBD CLI)

Run (HTTP)
- `uvicorn <package>.http.app:app --port 3000`
- Expose to Slack if needed or deploy behind HTTPS

Testing
- `pytest -q`
- Unit tests mock Slack clients; no external calls

Slack App Manifest
- See `docs/slack-app-manifest.yml` for a baseline manifest; adjust scopes to the plugins you enable.

Database & Migrations
- Set `DATABASE_URL` (Postgres/Neon) in `.env`.
- Apply migrations: `zebras db upgrade` (uses `alembic.ini` + `migrations/`).
- Roll back: `zebras db downgrade base`.
