**Testing Guide**

Unit Tests (planned)
- Router and middleware behaviors
- Signature verification for HTTP endpoints
- Logging plugin event handling
- Rules engine decisions

Manual Testing
- Socket Mode: `zebras socket` and trigger Slack events
- HTTP Events: `curl` examples
  - Events:
    - `curl -X POST localhost:3000/slack/events -H 'Content-Type: application/json' -d '{"type":"event_callback","event":{"type":"message","user":"U123","channel":"C123","text":"hi"}}'`
  - Slash commands:
    - `curl -X POST localhost:3000/slack/commands -H 'Content-Type: application/x-www-form-urlencoded' --data 'command=%2Frules&text=list'`

Database Verification
- After running `zebras db upgrade`, verify persisted logs:
  - `SELECT event_type, channel_id, user_id, created_at FROM event_logs ORDER BY id DESC LIMIT 10;`

