**Rules Plugin**

Purpose
- Provide message governance: thread lockdowns, bot posting restrictions, channel posting controls, with audit logs.

Current State
- Slash command `/rules` with: `list`, `bots on|off`, `top on|off`, `threads on|off`, and `manage` (opens a simple modal).
- Enforcement active on `message` events:
  - Blocks bot messages if disabled (and privately notifies the user).
  - Blocks top‑level posts if disabled (asks users to reply in threads).
  - Blocks thread replies if disabled.
- Audit messages sent to the configured audit channel (if set in Invite Helper settings); failures are tolerated.

Configuration
- Use `/rules` in-channel to view or change rules.
- Or use the Admin web UI (HTTP mode) to set per‑channel defaults.

Notes
- Deleting third‑party bot messages may be restricted by Slack; the plugin handles failures gracefully by still notifying users and auditing.
