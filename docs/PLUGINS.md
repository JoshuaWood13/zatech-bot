**Plugin System**

Plugins encapsulate features and register capabilities with the core. They are discoverable, configurable, and testable in isolation.

**Concepts**
- Registration: Plugins expose a `register(Registry)` function that attaches handlers and schedules.
- Capabilities:
  - Events: `on(event_type, filters?)(handler)`
  - Commands: `slash('/name')(handler)`
  - Actions/Views: `action(callback_id)(handler)`, `view_submission(callback_id)(handler)`
  - Rules: `rules().add(policy)` hooks for message governance
  - Schedules: `cron(spec)(job)` or `interval(seconds)(job)`
- Lifecycle: `on_startup(ctx)` and `on_shutdown(ctx)` hooks (optional)

**Registration Example (pseudocode)**
```
def register(reg: Registry):
    @reg.events.on('message', subtype=None)
    async def log_message(ctx, event):
        await ctx.logger.info({'msg': 'message', 'user': event.user})

    @reg.commands.slash('/rules')
    async def rules_cmd(ctx, command):
        await ctx.respond(text='Rules help...')

    reg.schedules.cron('0 9 * * MON')(weekly_digest_job)
```

**Configuration**
- Plugins receive a namespaced config view `ctx.config.plugins['my_plugin']`.
- Required config should be validated at startup; fail fast with clear errors.

**Packaging & Discovery**
- Local plugins live under `src/<package>/plugins/` and are auto-discovered.
- External plugins can advertise entry points `myframework.plugins` in `pyproject.toml`.

**Rules Engine**
- Policies are pure functions or dataclass-driven evaluators that receive `Context`, `Message`, `Channel`, and return Allow/Deny with reason.
- Execution order: deny > allow; short-circuit on explicit outcomes; all decisions logged with audit metadata.
- Built-in policies: thread lockdowns, channel-level posting controls, bot posting restrictions.

**Testing**
- Plugins include unit tests that mock Slack and storage interfaces.
- Provide payload fixtures and a thin `TestHarness` for driving events/commands.

