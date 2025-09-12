# ADR 0002: Plugin architecture

Status: Proposed

Context
- We need a modular way to add features like logging, rules, invite helpers without coupling to the core.

Decision
- Implement a registry-driven plugin API with capabilities: events, commands, actions/views, rules, schedules.
- Plugins register via a `register(registry)` function; discovery via `importlib.metadata` entry points.
- Provide a small DI context (`ctx`) with logger, config, slack client, stores, and job enqueuer.

Consequences
- Features ship as independent packages; core remains stable.
- Easy testing and per-plugin configuration.
- Clear surface for docs and examples.

