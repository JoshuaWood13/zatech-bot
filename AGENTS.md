# AGENTS.md — Repo Guidance for Agents and Contributors

This repository contains the legacy PHP app `SlackCommunityHelper` and a new initiative to redesign and recreate the Slack bot framework in Python. This document gives concrete guidance to coding agents and human contributors working within this repo.

Scope: This file applies to the entire repository unless a more-specific AGENTS.md is added in a subdirectory.

## Goals

- Build a modern, modular Python Slack framework inspired by SlackCommunityHelper’s capabilities.
- Emphasize maintainability, clear plugin boundaries, and strong testing.
- Keep legacy PHP app untouched except for reference. New work lives under `docs/` and future `python/` or `src/` paths.

## Source Layout (planned)

- `docs/` — Architecture, plans, ADRs, security, dev setup, Slack app manifest examples.
- `src/` (to be added) — Python framework source (`package` TBD after initial scaffolding).
- `examples/` (optional) — Example bots that consume the framework.
- `SlackCommunityHelper/` — Legacy Laravel/PHP app (read-only for reference).

## Coding Conventions (Python)

- Python ≥ 3.11, prefer async-first design.
- Use type hints everywhere; enable strict mypy in CI.
- Lint with ruff/flake8; format with black.
- Configuration via environment variables using pydantic-settings.
- Favor composition over inheritance; keep modules small and testable.
- Public APIs documented with docstrings and minimal README snippets.

## Architectural Tenets

- Adapter pattern for Slack I/O (Events API over HTTP and Socket Mode). HTTP via FastAPI; background tasks via Celery/RQ/Arq (TBD by ADRs).
- Event router + middleware pipeline for logging, auth, dedupe, rate-limit safety.
- Plugin system with clear capabilities (commands, actions, events, scheduled jobs, rules engine hooks).
- Storage abstraction (Redis/Postgres/SQLite) behind interfaces; no direct vendor calls in plugins.
- Observability by default: structured logging, metrics hooks, request IDs, error reporting surface.

## Testing

- Unit tests for all core modules and plugins.
- Lightweight fixtures for Slack payloads; snapshot key contracts.
- Do not call external Slack APIs in unit tests; mock Slack client.
- Provide a small integration test harness for end-to-end with fake Slack server.

## Security

- Never log secrets (bot tokens, signing secrets, app tokens).
- Verify Slack request signatures on all HTTP endpoints.
- Store tokens in env or secret manager; support rotation.
- Implement idempotency and replay protection in the router.

## How to Contribute (short)

- Add or edit docs in `docs/` keeping sections concise and actionable.
- Propose architecture changes via ADRs in `docs/ADRs/`.
- Keep patches focused; avoid touching legacy PHP unless necessary.
- Prefer adding examples to demonstrate new APIs over lengthy docs.

## What to Build First

Follow the roadmap in `docs/ROADMAP.md`. In short:

1) Minimal core + Slack adapter + router + plugin loader
2) Event logging plugin (users/channels/messages)
3) Rules engine for message governance
4) Invite helper + auto-join capabilities

