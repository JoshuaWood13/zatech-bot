**Roadmap**

Phase 0 — Foundations (Week 1–2)
- ADRs: async stack, worker, storage abstractions
- Create skeleton: config, logging, adapter interfaces, router, registry
- Socket Mode adapter MVP

Phase 1 — Core + Logging (Week 3–4)
- Event normalization and middleware (trace, metrics, idempotency)
- Plugin loader and reference Logging plugin (users/channels/messages)
- Basic persistence (SQLite for logs), metrics scaffolding

Phase 2 — Rules Engine (Week 5–6)
- Policy DSL + evaluation runtime
- Built-ins: thread lockdowns, bot restrictions, channel posting controls
- Violation audit logs to configured channel

Phase 3 — Helpers (Week 7–8)
- Invite Helper flows (notify admins, guide users)
- Auto-Join new channels configuration
- Admin slash commands for rules and helpers

Phase 4 — HTTP Events + Interactivity (Week 9–10)
- FastAPI endpoints with signature verification
- View submissions, actions, and modals support
- Optional deployment guide and manifests

Phase 5 — Hardening (Week 11–12)
- Rate limit backoff, retry strategy, DLQ
- Multi-workspace tenancy, token rotation
- Observability polish (dashboards, tracing hooks)

Stretch Goals
- Moderation queue plugin; scheduled digests; karma system
- Import/export of rules as code; plugin marketplace shape

