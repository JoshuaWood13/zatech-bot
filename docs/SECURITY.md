**Security Guide**

Secrets
- Keep `SLACK_BOT_TOKEN`, `SLACK_SIGNING_SECRET`, `SLACK_APP_TOKEN` out of logs.
- Load via env or secret manager; support rotation and hot-reload where possible.

Request Validation (HTTP)
- Verify Slack signature using signing secret and timestamp.
- Enforce 5-minute replay window; reject stale or skewed requests.
- Respond to `url_verification` challenges correctly.

Idempotency & Replay Protection
- Compute idempotency key from event `event_id` and `event_time`.
- Maintain a short-lived set to drop duplicates.

Permissions & Scopes
- Use least-privilege OAuth scopes per plugin needs (e.g., `channels:read`, `chat:write`, `commands`).
- Map admin-only commands to workspace roles/user allowlists.

Data Handling
- Redact PII in logs; opt-in for any storage of message bodies beyond required auditing.
- Configurable retention windows; delete on request where feasible.

Operational Security
- Rotate tokens regularly; check for scope drift.
- Protect admin commands with confirmation steps for destructive actions.
- Provide a security mode toggle to elevate logging and alerts.

Dependencies & Supply Chain
- Pin versions; use `pip-tools` or `uv` lockfiles.
- Enable vulnerability scans in CI.

