**CLI Reference (`zebras`)**

Commands
- `zebras socket`
  - Runs the Socket Mode app. Requires `SLACK_APP_TOKEN`.
- `zebras http [--host HOST] [--port PORT]`
  - Runs the HTTP Events/Commands server. Requires `SLACK_SIGNING_SECRET` for production.
- `zebras worker [--queue NAME]`
  - Starts an RQ worker against `REDIS_URL`. Queue default: `zebras`.

Database
- `zebras db upgrade [REVISION]`
  - Apply migrations up to `REVISION` (default `head`).
- `zebras db downgrade [REVISION]`
  - Downgrade to `REVISION` (default `base`).

Notes
- CLI loads configuration from `.env` and environment variables.
- Use `LOG_LEVEL=DEBUG` to increase verbosity.

