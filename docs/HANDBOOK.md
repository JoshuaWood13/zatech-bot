# ZEBRAS Slack Bot — Noob Handbook

Welcome! This is a simple, human-friendly guide to what the ZEBRAS Slack bot does today and how you can use it without knowing any code or internals.

## What It Can Do Today

Right now, the bot’s user-facing feature is an Auto‑Responder that can reply to messages when certain phrases appear. You can manage these rules directly in Slack using the `/auto` slash command. When a rule matches a message:

- The bot posts a helpful reply in a thread under the message.
- It responds at most once per message.
- It ignores non-user “system” messages (like join/rename notices).

If your admins enabled the web admin page, you may also see a simple browser UI for viewing and editing rules. Ask an admin for the URL if applicable.

## Auto‑Responder: Quick Commands

Use these in any channel where the bot is installed:

- Add a rule
  - `/auto add phrase:"how do I join" reply:"See #introductions for details" match:contains scope:here`
  - Options:
    - `phrase:"..."` — text to match
    - `reply:"..."` — what the bot will say
    - `match:` — `contains` (default), `exact`, or `regex`
    - `scope:` — `here` (this channel only) or `global` (all channels)
    - `case:` — `on` or `off` (default off)

- List rules
  - `/auto list` — shows rules affecting this channel (channel + global)
  - `/auto list global` — shows only global rules

- Enable/disable a rule by ID
  - `/auto enable 42`
  - `/auto disable 42`

- Delete a rule by ID
  - `/auto delete 42`

Tips
- “Global” rules apply everywhere; “here” limits to the current channel.
- Use quotes around phrases and replies that contain spaces.
- Regex is powerful but easy to get wrong — start with `contains` unless you’re sure.

## What You Might See (If Enabled by Admins)

The codebase includes a few extra capabilities that your workspace owners can turn on. If they’re enabled, you’ll see these commands or behaviors:

- Channel Rules (`/rules`)
  - Control per‑channel posting policy (allow/block bot messages, top‑level posts, or thread replies).
  - Examples:
    - `/rules list` — show current rules for this channel
    - `/rules bots on|off`, `/rules top on|off`, `/rules threads on|off`
    - `/rules manage` — open a simple settings modal
  - When a rule is violated, the bot sends an ephemeral (only you can see it) nudge and may audit to a configured channel.

- Invite Helper (`/invite-helper`)
  - DM onboarding message to new members and/or notify an admin channel when someone joins.
  - Examples:
    - `/invite-helper set-channel #admins`
    - `/invite-helper notify on|off`
    - `/invite-helper message Welcome to the community! Please read #rules.`

- App Home (`/zebras-home`)
  - Shows a simple “ZEBRAS Admin” Home tab with a button to open settings.

- Event Logging (no command)
  - Records key Slack events (messages, channel changes, user joins/updates) to a database for moderation/analytics.

Note: In many deployments only the Auto‑Responder is enabled initially. If a command like `/rules` or `/invite-helper` says “not found” or does nothing, it’s likely not enabled in your workspace yet.

## Web Admin Page (Optional)

If your admins run the HTTP mode, a basic admin page may be available at a URL they will share. It typically includes:

- Invite Helper settings (admin/audit channels, onboarding DM text, notify on join)
- Per‑channel posting rules (bots, top posts, threads)
- Auto‑Responder: add/list/toggle/delete rules (global or per‑channel)

Changes you make here take effect immediately. Depending on your workspace, some sections may be visible but not active if the corresponding feature isn’t enabled yet.

## Troubleshooting

- “Unknown command” when using `/auto`
  - The slash command may not be installed for your workspace or the bot is offline. Ask an admin to check the app setup and that the bot is running.

- Bot didn’t reply to a matching message
  - Check with `/auto list` to confirm the rule exists and is enabled for this channel.
  - The message might not match exactly (case, punctuation, or regex mismatch).
  - The bot replies only to normal user messages, and only once per message.

- I don’t see `/rules` or `/invite-helper`
  - Those features may be disabled. Ask an admin if they’re planned for your workspace.

## Quick Health Check

- Use `/debug` anywhere to get a quick status readout (Slack auth, DB, Redis, and which slash commands are registered). The response is ephemeral, so only you will see it.

## Quick Facts

- The bot only acts in channels where it’s installed/invited.
- Replies for auto‑responses are posted in a thread to reduce noise.
- Use quotes in `/auto` for phrases/replies with spaces.
- Global rules affect all channels; “here” limits to the current channel.

Need help? Ask in your workspace’s bot/help channel or ping an admin.
