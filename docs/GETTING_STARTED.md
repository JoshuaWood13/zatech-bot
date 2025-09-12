**Getting Started**

Prerequisites
- Python 3.11+
- Slack app created and installed (use `docs/slack-app-manifest.yml` as a base)
- Postgres reachable (local or Neon) and optionally Redis for worker

Install
- `pip install -e .` (from repo root)
- Copy `.env.example` to `.env` and set required values

Run (Socket Mode)
- Set `SLACK_BOT_TOKEN` and `SLACK_APP_TOKEN`
- `zebras socket`
- In Slack, type `/rules` to verify command handling

Run (HTTP Events)
- Set `SLACK_BOT_TOKEN` and `SLACK_SIGNING_SECRET`
- `zebras http --port 43117` (or set `PORT`)
- Slack Event Subscriptions → `https://<host>/slack/events`
- Slash Commands → `https://<host>/slack/commands`

Database
- Set `DATABASE_URL` (Postgres/Neon DSN)
- Apply migrations: `zebras db upgrade`
- Verify logs: `SELECT * FROM event_logs ORDER BY id DESC LIMIT 5;`

Worker (optional)
- Ensure `REDIS_URL` points to a running Redis
- `zebras worker`

Troubleshooting
- Increase verbosity: set `LOG_LEVEL=DEBUG`
- Socket Mode: ensure the app has `SLACK_APP_TOKEN` and Socket Mode enabled
- HTTP: ensure signature verification keys and HTTPS exposure are correct
