**ZEBRAS Parity TODOs**

Status: living checklist to reach feature parity with SlackCommunityHelper. Use this as a lightweight project board. Tags: [P0]=Critical, [P1]=High, [P2]=Nice-to-have.

**Core Platform**
- [ ] [P0] Plugin discovery via entry points (external plugins)
- [ ] [P0] Middleware: request IDs, structured logging context
- [ ] [P0] Middleware: idempotency / dedupe (event_id + window)
- [ ] [P0] Slack API client wrapper with 429 backoff + retries
- [ ] [P1] Metrics hooks (StatsD/OTel) for events and errors
- [ ] [P1] Error reporting hook (Sentry-compatible interface)
- [ ] [P1] ACL for admin-only commands and actions

**Adapters**
- [x] [P0] Socket Mode: slash command dispatch
- [x] [P0] HTTP: slash command parsing + dispatch
- [ ] [P0] HTTP: interactivity endpoints (actions/views) with signature verify
- [ ] [P1] Health and readiness endpoints including dependency checks

**Storage & Worker**
- [x] [P0] SQLAlchemy models: event logs (message/user/channel)
- [ ] [P0] SQLAlchemy models: rules, policies, audit logs
- [x] [P0] Alembic migrations setup and first migration
- [ ] [P0] Redis-backed idempotency set and locks
- [ ] [P1] RQ job enqueue + helpers (retry policy, DLQ routing)
- [ ] [P2] Scheduler (rq-scheduler or APScheduler) for periodic jobs

**Feature: Logging Events**
- [ ] [P0] Message Delete Log (message_deleted)
- [ ] [P0] Message Update Log (message_changed)
- [ ] [P0] User Update Log (user_change)
- [ ] [P0] User Joined Log (team_join / member_joined_channel)
- [ ] [P0] Channel Event Log (create/rename/delete/archive/unarchive)
- [x] [P1] Persist logs to Postgres with minimal schema
- [ ] [P1] Optional: redact PII fields per configuration

**Feature: Message Rules**
- [ ] [P0] Thread lockdowns (allow/deny lists)
- [ ] [P0] Bot posting restrictions in configured channels
- [ ] [P0] Channel posting controls: top-level vs thread permissions
- [ ] [P0] Violation handling: delete/soft actions + audit log to channel
- [x] [P0] Admin slash command `/rules` to list/enable/disable (stub implemented)
- [ ] [P1] Rules persistence + import/export
- [ ] [P1] Exemption lists and role mapping

**Feature: Invite Helper**
- [ ] [P1] Notify admins on invite attempts (configurable)
- [ ] [P1] Guidance DM to users attempting invites
- [ ] [P1] Admin workflows via actions/modals (approve/deny)

**Feature: Auto-Join New Channels**
- [ ] [P1] Detect new channels and auto-join bot
- [ ] [P2] Optional: auto-join specific users or groups (where permitted)

**CLI & Dev UX**
- [ ] [P1] `zebras plugins list` and `zebras plugins doctor`
- [ ] [P1] `zebras db migrate` and `zebras db upgrade`
- [ ] [P2] `zebras manifest render` from enabled plugins/scopes

**Security**
- [ ] [P0] Ensure no secrets in logs (redaction tests)
- [ ] [P0] Enforce signature verification for all HTTP endpoints
- [ ] [P1] Token rotation support (reload without restart)

**Testing**
- [ ] [P0] Unit tests: router, middleware, signature verification
- [ ] [P0] Unit tests: logging plugin event coverage
- [ ] [P0] Unit tests: rules engine decisions (allow/deny/neutral)
- [ ] [P1] Integration: fake Slack payloads through adapters to DB
- [ ] [P1] Load tests for high event volume (basic)

**Docs**
- [ ] [P0] Update `docs/PLUGINS.md` with slash/interaction examples
- [ ] [P0] Add `docs/RULES.md` with policy DSL and examples
- [ ] [P1] Deployment guide (Docker, Neon Postgres, Redis)
- [ ] [P1] Security runbook and hardening checklist

**Parity Tracking**
- [ ] Logging parity achieved (all event types covered and persisted)
- [ ] Rules parity achieved (thread/channel/bot restrictions + audit)
- [ ] Invite Helper parity achieved
- [ ] Auto-Join parity achieved

Notes
- Neon Postgres: use its DSN directly in `DATABASE_URL`.
- Worker: RQ selected for simplicity; plug-in alternative later via interface if needed.

**Completed**
- [x] Project scaffold: `pyproject.toml`, CLI entrypoint, `.env.example`, README
- [x] Async core router and plugin registry skeleton
- [x] Socket Mode adapter wired to router for events
- [x] HTTP app with `/healthz` and `/slack/events` + signature verification; `/slack/commands` placeholder endpoint
- [x] Redis and Postgres factories (Redis client + SQLAlchemy async engine)
- [x] RQ worker starter and CLI command
- [x] Reference Logging plugin (basic handlers for message, channel events, user changes/joins; stdout logging only)
