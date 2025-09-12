**Logging Plugin**

Purpose
- Capture key Slack events for community moderation and observability.

Events Covered (now)
- Message: `message` (including subtype metadata)
- Channels: `channel_created`, `channel_rename`, `channel_deleted`, `channel_archive`, `channel_unarchive`
- Users: `team_join`, `user_change`

Behavior
- Logs structured info to stdout via Python logging.
- Persists each event into `event_logs` (JSONB `raw` + normalized fields).

Configuration
- None required currently. Future options: redaction rules, target channels for audit notifications.

Extending
- Add new `@registry.events.on('<event>')` handlers in `src/zebras/plugins/logging/__init__.py`.

