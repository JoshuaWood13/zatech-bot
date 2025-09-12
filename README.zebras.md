# ZEBRAS – ZaTech Engagement Bot for Responses, Automation & Support

ZEBRAS is a modular Python framework for building Slack community helpers, inspired by SlackCommunityHelper. It focuses on extensibility via plugins, safe-by-default middleware, and strong observability.

Highlights
- Async-first core with Socket Mode and HTTP Event adapters
- Plugin system for events, commands, actions/views, rules, and schedules
- Postgres + Redis by default; easy to point at Neon Postgres via DSN
- RQ worker for simple background jobs

Quick Start
1. Create a Slack app and install it (see `docs/slack-app-manifest.yml`).
2. Copy `.env.example` to `.env` and set tokens/URLs.
3. Socket Mode: `zebras socket` (recommended for local, requires `SLACK_APP_TOKEN`)
4. HTTP API: `zebras http --port 43117` (or set `PORT`, requires public HTTPS + `SLACK_SIGNING_SECRET`)
5. Worker (optional): `zebras worker` (RQ; Redis must be running)

Docs
- Architecture: `docs/ARCHITECTURE.md`
- Plugins: `docs/PLUGINS.md`
- Security: `docs/SECURITY.md`
- Development: `docs/DEVELOPMENT.md`
 - Deployment (Docker): `docs/DEPLOYMENT.md`

Setup Details
- Python: 3.11+
- Env vars (`.env`):
  - `SLACK_BOT_TOKEN` (xoxb-)
  - `SLACK_APP_TOKEN` (xapp-, for Socket Mode)
  - `SLACK_SIGNING_SECRET` (for HTTP endpoints)
  - `DATABASE_URL` (e.g., `postgresql+asyncpg://user:pass@host:5432/zebras`; Neon DSN works)
  - `REDIS_URL` (e.g., `redis://localhost:6379/0`)
  - `ZEBRAS_HTTP_HOST`/`ZEBRAS_HTTP_PORT` (defaults: 0.0.0.0:3000)

Slack Manifest
- Use `docs/slack-app-manifest.yml` as a baseline. Ensure:
  - Socket Mode enabled (for local dev) or Event Subscriptions set to your HTTPS URL
  - Interactivity request URL set if you plan to use actions/views
  - Scopes include: `commands`, `chat:write`, `channels:read`, `channels:history`, etc.

Running (Socket Mode)
- Ensure `.env` has `SLACK_BOT_TOKEN` and `SLACK_APP_TOKEN`.
- Start: `zebras socket`
- Generate events by posting messages; the Logging plugin prints to stdout.
- Test slash command: in Slack, type `/rules` → you should get an ephemeral reply.

Verify Persistence
- Ensure you ran `zebras db upgrade` and set `DATABASE_URL`.
- Generate a few events (post a message, rename a channel, etc.).
- Check the DB (example): `SELECT event_type, channel_id, user_id, created_at FROM event_logs ORDER BY id DESC LIMIT 10;`

Running (HTTP Events)
- Ensure `.env` has `SLACK_BOT_TOKEN` and `SLACK_SIGNING_SECRET`.
- Start: `zebras http --port 43117` (or export `PORT=43117`)
- Point Slack Event Subscriptions to `https://<host>/slack/events` (URL verification handled).
- Slash commands URL: `https://<host>/slack/commands`.
- Admin UI (no auth): Visit `https://<host>/` to configure Invite Helper and per-channel rules.
- Local test (no signature):
  - `curl -X POST localhost:43117/slack/events -H 'Content-Type: application/json' -d '{"type":"event_callback","event":{"type":"message","user":"U123","channel":"C123","text":"hi"}}'`
  - `curl -X POST localhost:43117/slack/commands -H 'Content-Type: application/x-www-form-urlencoded' --data 'command=%2Frules&text=list'`

Persistence
- Postgres via SQLAlchemy async engine is used by the Logging plugin to persist events.
- Migrations: run `zebras db upgrade` (uses `alembic.ini` and `migrations/`).
- Neon: paste your Neon DSN into `DATABASE_URL`; no code changes required.
- Upcoming: rules and audit tables + persistence.

Extending
- Add plugins under `src/zebras/plugins/<name>/` and expose a `register(registry)` function.
- Register events using `@registry.events.on('message')`; slash commands with `@registry.commands.slash('/name')`.

Limitations (current)
- Slash commands are wired; actions/views are pending.
- Idempotency/rate-limit middleware and rules enforcement are in progress.
Docker Quick Start
- HTTP mode: `docker compose up --build zebras-http` (exposes `http://localhost:43117`).
- Admin UI: open `http://localhost:43117/`.
- Socket mode: `docker compose up --build zebras-socket`.
- Worker: `docker compose up --build zebras-worker`.
- Set Slack envs in a top-level `.env` file or export them before running compose.
