from __future__ import annotations

from typing import Dict, Any, Optional

from ...plugin import Registry
from ...app_context import get_context
from ...rules.repository import ChannelRuleRepository
from ...storage.repositories import EventLogRepository
from slack_sdk.models.views import View
from slack_sdk.web.async_client import AsyncWebClient


def register(reg: Registry) -> None:
    async def _client() -> AsyncWebClient:
        ctx = get_context()
        return await ctx.web_client()

    @reg.commands.slash("/rules")
    async def rules_cmd(payload: Dict[str, Any]) -> Dict[str, Any]:
        text = (payload.get("text") or "").strip()
        channel_id = payload.get("channel_id")
        user_id = payload.get("user_id")
        ctx = get_context()
        repo = ChannelRuleRepository(ctx.engine)

        if text.startswith("bots "):
            val = text.split(" ", 1)[1].lower() in ("on", "true", "allow")
            await repo.upsert(channel_id, allow_bots=val)
            return {"response_type": "ephemeral", "text": f"Bots {'allowed' if val else 'blocked'} in <#{channel_id}>"}
        if text.startswith("top "):
            val = text.split(" ", 1)[1].lower() in ("on", "true", "allow")
            await repo.upsert(channel_id, allow_top_level_posts=val)
            return {"response_type": "ephemeral", "text": f"Top-level posts {'allowed' if val else 'blocked'} in <#{channel_id}>"}
        if text.startswith("threads "):
            val = text.split(" ", 1)[1].lower() in ("on", "true", "allow")
            await repo.upsert(channel_id, allow_thread_replies=val)
            return {"response_type": "ephemeral", "text": f"Thread replies {'allowed' if val else 'blocked'} in <#{channel_id}>"}
        if text == "list":
            r = await repo.get(channel_id)
            if not r or not hasattr(r, "allow_bots"):
                return {"response_type": "ephemeral", "text": "No rules set. Defaults: bots ON, top-level ON, threads ON"}
            return {
                "response_type": "ephemeral",
                "text": f"Rules for <#{channel_id}> — bots: {'ON' if r.allow_bots else 'OFF'}, top: {'ON' if r.allow_top_level_posts else 'OFF'}, threads: {'ON' if r.allow_thread_replies else 'OFF'}",
            }
        if text == "manage":
            # Minimal placeholder modal
            trigger_id = payload.get("trigger_id")
            client = await _client()
            # Preload current values
            r = await repo.get(channel_id)
            bots_on = (r.allow_bots if r else True)
            top_on = (r.allow_top_level_posts if r else True)
            threads_on = (r.allow_thread_replies if r else True)
            view = {
                "type": "modal",
                "callback_id": "rules_manage",
                "title": {"type": "plain_text", "text": "ZEBRAS Rules"},
                "close": {"type": "plain_text", "text": "Close"},
                "submit": {"type": "plain_text", "text": "Save"},
                "private_metadata": channel_id,
                "blocks": [
                    {"type": "input", "block_id": "bots",
                     "element": {"type": "static_select", "action_id": "val",
                                  "options": [
                                      {"text": {"type": "plain_text", "text": "Allow"}, "value": "on"},
                                      {"text": {"type": "plain_text", "text": "Block"}, "value": "off"},
                                  ],
                                  "initial_option": {"text": {"type": "plain_text", "text": ("Allow" if bots_on else "Block")}, "value": ("on" if bots_on else "off")}
                                  },
                     "label": {"type": "plain_text", "text": "Bot messages"}},
                    {"type": "input", "block_id": "top",
                     "element": {"type": "static_select", "action_id": "val",
                                  "options": [
                                      {"text": {"type": "plain_text", "text": "Allow"}, "value": "on"},
                                      {"text": {"type": "plain_text", "text": "Block"}, "value": "off"},
                                  ],
                                  "initial_option": {"text": {"type": "plain_text", "text": ("Allow" if top_on else "Block")}, "value": ("on" if top_on else "off")}
                                  },
                     "label": {"type": "plain_text", "text": "Top-level posts"}},
                    {"type": "input", "block_id": "threads",
                     "element": {"type": "static_select", "action_id": "val",
                                  "options": [
                                      {"text": {"type": "plain_text", "text": "Allow"}, "value": "on"},
                                      {"text": {"type": "plain_text", "text": "Block"}, "value": "off"},
                                  ],
                                  "initial_option": {"text": {"type": "plain_text", "text": ("Allow" if threads_on else "Block")}, "value": ("on" if threads_on else "off")}
                                  },
                     "label": {"type": "plain_text", "text": "Thread replies"}},
                ],
            }
            await client.views_open(trigger_id=trigger_id, view=view)
            return {"response_type": "ephemeral", "text": "Opened rules manager."}

        return {
            "response_type": "ephemeral",
            "text": "Usage: /rules list | bots on|off | top on|off | threads on|off | manage",
        }

    @reg.interactions.view_submission("rules_manage")
    async def rules_manage_submit(payload: Dict[str, Any]) -> None:
        channel_id = payload.get("view", {}).get("private_metadata")
        state = payload.get("view", {}).get("state", {}).get("values", {})
        def _val(block_id: str) -> Optional[bool]:
            try:
                selected = state[block_id]["val"]["selected_option"]["value"]
                return selected == "on"
            except Exception:
                return None
        bots = _val("bots")
        top = _val("top")
        threads = _val("threads")
        ctx = get_context()
        repo = ChannelRuleRepository(ctx.engine)
        await repo.upsert(channel_id, allow_bots=bots, allow_top_level_posts=top, allow_thread_replies=threads)

    @reg.events.on("message")
    async def enforce_rules(payload: Dict[str, Any]) -> None:
        e = payload.get("event", payload)
        channel = e.get("channel")
        if not channel:
            return
        ctx = get_context()
        repo = ChannelRuleRepository(ctx.engine)
        rules = await repo.get(channel)
        if not rules or not hasattr(rules, "allow_bots"):
            return
        subtype = e.get("subtype")
        ts = e.get("ts")
        user = e.get("user")
        thread_ts = e.get("thread_ts")
        client = await _client()

        # Helper to audit
        async def audit(msg: str) -> None:
            from ..invite.repository import InviteSettingsRepository
            srepo = InviteSettingsRepository(ctx.engine)
            s = await srepo.get()
            audit_ch = s.audit_channel_id if s else None
            if audit_ch:
                try:
                    await client.chat_postMessage(channel=audit_ch, text=msg)
                except Exception:
                    pass

        # 1) Block bots
        if subtype == "bot_message" and not rules.allow_bots:
            # Bot messages can be deleted by the bot
            try:
                await client.chat_delete(channel=channel, ts=ts)
            except Exception:
                pass
            await client.chat_postEphemeral(channel=channel, user=user, text="Bot messages are not allowed in this channel.")
            await audit(f"Rule(bots) in <#{channel}> triggered by <@{user}> at {ts}")
            return

        # 2) Block top-level posts
        if not thread_ts and not rules.allow_top_level_posts:
            await client.chat_postEphemeral(channel=channel, user=user, text="Top-level posts are disabled here. Please use a thread.")
            await audit(f"Rule(top) in <#{channel}> triggered by <@{user}> at {ts}")
            return

        # 3) Block thread replies
        if thread_ts and not rules.allow_thread_replies:
            await client.chat_postEphemeral(channel=channel, user=user, text="Thread replies are disabled here.")
            await audit(f"Rule(threads) in <#{channel}> triggered by <@{user}> at {ts}")
            return
