**Rules Plugin (Stub)**

Purpose
- Provide message governance: thread lockdowns, bot posting restrictions, channel posting controls, with audit logs.

Current State
- Slash command `/rules` implemented with a minimal stub (help and `list`).
- No enforcement yet; evaluation engine scaffold exists in `src/zebras/rules/engine.py`.

Planned
- Policies: thread lockdowns (allow/deny lists), bot restrictions, channel posting rules.
- Actions: delete/soft actions on violations and audit logging to DB and a configured channel.
- Admin: interactive modals and a Home tab to manage rules.

CLI/UX
- `/rules` → help and list placeholders. Future: `enable/disable <rule>` and configuration flows.

