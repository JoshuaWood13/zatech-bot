**Adapters: Socket Mode and HTTP**

Socket Mode
- Websocket connection via Slack’s Socket Mode; no public HTTP required.
- Requirements: `SLACK_BOT_TOKEN`, `SLACK_APP_TOKEN`, and Socket Mode enabled in the Slack app.
- Handles: Events API payloads, slash commands (dispatched via response_url).
- Run: `zebras socket`

HTTP (Events API + Commands)
- ASGI app built with FastAPI.
- Endpoints:
  - `POST /slack/events`: Event Subscriptions (handles `url_verification`).
  - `POST /slack/commands`: Slash commands (form-encoded).
  - `GET /healthz`: Liveness probe.
- Signature verification enforced when `SLACK_SIGNING_SECRET` is set.
- Run: `zebras http --port 43117` (or set `PORT`) and expose via HTTPS or a tunnel in dev.

Slack Configuration
- Use `docs/slack-app-manifest.yml` to bootstrap scopes and events.
- For HTTP mode, set request URLs in Slack to your public endpoints.
