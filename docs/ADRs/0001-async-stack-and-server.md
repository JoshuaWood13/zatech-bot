# ADR 0001: Async stack and server

Status: Proposed

Context
- We need an async-first framework that supports both Socket Mode and HTTP Events API with interactivity.

Decision
- Use FastAPI for HTTP endpoints (async, type-friendly, good ecosystem).
- Use `slack_sdk` for Web API client and Socket Mode. Evaluate `bolt-python` for parity but keep our own router and plugin model.
- Adopt `pydantic`/`pydantic-settings` for config and validation.

Consequences
- Lean core, minimal vendor lock-in for routing/middleware.
- Easy to integrate with ASGI servers and middlewares.
- Clear, testable boundaries.

