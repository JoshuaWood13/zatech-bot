**Configuration**

Environment Variables
- `SLACK_BOT_TOKEN` (required): Bot token (xoxb-…)
- `SLACK_APP_TOKEN` (socket mode): App-level token (xapp-…)
- `SLACK_SIGNING_SECRET` (HTTP mode): For signature verification
- `SLACK_CLIENT_ID` and `SLACK_CLIENT_SECRET` (optional): For OAuth installs if you build web flows later
- `SLACK_VERIFICATION_TOKEN` (optional): Legacy verification token (not required when using signatures)
- `ZEBRAS_MODE` (optional): `socket` or `http` (defaults to socket)
- `ZEBRAS_HTTP_HOST` / `ZEBRAS_HTTP_PORT`: HTTP bind (defaults 0.0.0.0:3000)
- `REDIS_URL`: Redis connection (default `redis://localhost:6379/0`)
- `DATABASE_URL`: Postgres DSN (e.g., `postgresql+asyncpg://user:pass@host:5432/zebras`)
- `LOG_LEVEL`: INFO, DEBUG, etc.

Neon Postgres
- Use Neon’s provided DSN directly as `DATABASE_URL` — no code changes required.

Slack App
- Use `docs/slack-app-manifest.yml` as a starting point; enable Socket Mode or set Events/Interactivity URLs.
