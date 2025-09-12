**Architecture Overview**

This project redesigns the SlackCommunityHelper app into a modern, modular Python framework suitable for community management bots. It uses an async-first core, clear extension points, and first-class observability.

**Goals**
- Community operations at scale: event logging, message rules, invite mitigation, auto-join.
- Clean separation of concerns via adapters, router, and plugins.
- Simple local dev via Socket Mode, optional HTTP for Events API.
- Safe-by-default: signature verification, idempotency, retries, rate-limit aware.

**Non-Goals**
- Not a monolith app. It’s a framework plus reference plugins.
- Not tied to a single database; storage is pluggable.

**Core Components**
- App Core: Async runtime and lifecycle (startup/shutdown), config loading, dependency container.
- Slack Adapter:
  - HTTP (FastAPI) for Events API and Interactivity.
  - Socket Mode for local/dev or when inbound HTTP is not feasible.
- Event Router: Normalizes Slack payloads, validates signatures (HTTP), deduplicates events, applies middleware, dispatches to handlers.
- Middleware: Logging, trace context, metrics, idempotency/replay protection, permission gates, rate limit backoff.
- Plugin System: Discoverable units that register handlers for events, slash commands, actions, shortcuts, scheduled jobs, and rules engine hooks.
- Rules Engine: Declarative policies for who can post where (top-level vs thread), bot restrictions, allow/deny lists, with audit logs on violations.
- Storage Layer: Interfaces for key-value (Redis/Memcached) and relational/SQL (Postgres/SQLite). Used by rules, logs, state, and schedules.
- Background Jobs: Offload heavy work and retries (Celery/RQ/Arq). Scheduling supports cron-like and delayed jobs.
- Observability: Structured logs, metrics hooks (StatsD/OTel), error reporting hook (Sentry-compatible), request/trace IDs.

**Data Flow (Socket Mode)**
1) Slack websocket delivers events to Adapter
2) Router normalizes, assigns `request_id`, checks dedupe and ACL
3) Middleware runs (logging, metrics, idempotency)
4) Handlers executed (plugins); long tasks enqueued to background worker
5) Results and errors emitted to sinks (logs/metrics), responses posted via Slack Web API

**Data Flow (HTTP Events API)**
1) Slack POST -> FastAPI endpoint `/slack/events`
2) Verify Slack signature + timestamp, respond to `url_verification`
3) Router processes as above

**Plugin Capabilities**
- Event Handlers: `message`, `member_joined_channel`, `team_join`, `channel_*`, `user_change`, `message_changed/deleted`.
- Commands: `/rules`, `/invite-helper`, `/moderation`, etc.
- Actions/Shortcuts: Button/menu handlers, message actions, modals.
- Rules Engine Hooks: Evaluate policies on message create/update/delete and thread replies.
- Scheduled Jobs: Digests, cleanups, periodic syncs.

**Reference Plugins (Parity with SlackCommunityHelper)**
- Logging: User updates/joins; channel events (create/rename/delete/archive/unarchive); message delete/update.
- Message Rules: Thread lockdowns (allow/deny lists); bot posting restrictions; channel posting controls; violation logging to a channel.
- Invite Helper: Mitigate unrestricted invites (guidance, approvals, or notifications).
- Auto-Join: Auto-join configured channels for the bot or selected users/roles.

**Configuration**
- pydantic-settings loads from env or `.env` (local). Key vars: `SLACK_BOT_TOKEN`, `SLACK_SIGNING_SECRET`, `SLACK_APP_TOKEN` (for Socket Mode).
- Plugin configuration namespaces (e.g., `RULES_*`, `LOGGING_*`).

**Security**
- Signature verification (HTTP), replay window enforcement, idempotency keys.
- Token scoping (least privilege), optional token rotation.
- Redaction of sensitive fields in logs.

**Error Handling & Retries**
- Backoff on Slack rate limits (HTTP 429) via adapter wrapper.
- Retry transient storage/network errors in background tasks.
- Dead-letter queue for failing jobs with alert hooks.

**Persistence**
- Abstractions: `StateStore` (KV), `DataStore` (SQL), `LockProvider` (distributed locks), `Queue` (jobs).
- Default local stack: SQLite + Redis (or pure in-memory for dev).

**Dev Experience**
- Socket Mode-first to avoid tunneling.
- Optional FastAPI endpoints for Events/Interactivity; health checks at `/healthz`.
- CLI to run app, list plugins, validate config, render manifest.

**Extensibility**
- Entry-point based plugin discovery (`pkg_resources`/`importlib.metadata`).
- Declarative registration of handlers; lightweight DI for shared services.

**Open Questions**
- Which worker library: Celery vs RQ vs Arq? (See ADRs)
- Default storage combo and migrations.
- Built-in manifests vs per-deployment overrides.

