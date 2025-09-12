from __future__ import annotations

from typing import Any, Dict, Optional

from slack_sdk.web.async_client import AsyncWebClient

from ...plugin import Registry
from ...app_context import get_context
from ..invite.repository import InviteSettingsRepository


async def _client() -> AsyncWebClient:
    ctx = get_context()
    return await ctx.web_client()


def register(reg: Registry) -> None:
    @reg.events.on("app_home_opened")
    async def on_home_opened(payload: Dict[str, Any]) -> None:
        user = payload.get("event", {}).get("user")
        client = await _client()
        ctx = get_context()
        repo = InviteSettingsRepository(ctx.engine)
        s = await repo.get()
        admin_ch = s.admin_channel_id if s else None
        audit_ch = s.audit_channel_id if s else None
        notify = (s.notify_on_join if s else False)

        view = {
            "type": "home",
            "blocks": [
                {"type": "header", "text": {"type": "plain_text", "text": "ZEBRAS Admin"}},
                {"type": "section", "text": {"type": "mrkdwn", "text": "Quick settings and status"}},
                {"type": "section", "fields": [
                    {"type": "mrkdwn", "text": f"*Admin channel:* {'<#'+admin_ch+'>' if admin_ch else 'unset'}"},
                    {"type": "mrkdwn", "text": f"*Audit channel:* {'<#'+audit_ch+'>' if audit_ch else 'unset'}"},
                    {"type": "mrkdwn", "text": f"*Notify on join:* {'ON' if notify else 'OFF'}"},
                ]},
                {"type": "actions", "elements": [
                    {"type": "button", "action_id": "open_settings", "text": {"type": "plain_text", "text": "Open Settings"}},
                ]},
            ],
        }
        await client.views_publish(user_id=user, view=view)

    @reg.interactions.action("open_settings")
    async def open_settings(payload: Dict[str, Any]) -> None:
        trigger_id = payload.get("trigger_id")
        client = await _client()
        ctx = get_context()
        repo = InviteSettingsRepository(ctx.engine)
        s = await repo.get()
        view = {
            "type": "modal",
            "callback_id": "admin_settings",
            "title": {"type": "plain_text", "text": "ZEBRAS Settings"},
            "submit": {"type": "plain_text", "text": "Save"},
            "close": {"type": "plain_text", "text": "Cancel"},
            "blocks": [
                {"type": "input", "block_id": "admin_channel",
                 "element": {"type": "conversations_select", "action_id": "val",
                              "default_to_current_conversation": False,
                              **({"initial_conversation": s.admin_channel_id} if s and s.admin_channel_id else {})},
                 "label": {"type": "plain_text", "text": "Admin channel"}},
                {"type": "input", "block_id": "audit_channel",
                 "element": {"type": "conversations_select", "action_id": "val",
                              "default_to_current_conversation": False,
                              **({"initial_conversation": s.audit_channel_id} if s and s.audit_channel_id else {})},
                 "label": {"type": "plain_text", "text": "Audit channel"}},
                {"type": "input", "block_id": "notify",
                 "element": {"type": "static_select", "action_id": "val",
                              "options": [
                                  {"text": {"type": "plain_text", "text": "ON"}, "value": "on"},
                                  {"text": {"type": "plain_text", "text": "OFF"}, "value": "off"},
                              ],
                              **({"initial_option": {"text": {"type": "plain_text", "text": ("ON" if (s and s.notify_on_join) else "OFF")}, "value": ("on" if (s and s.notify_on_join) else "off")}})},
                 "label": {"type": "plain_text", "text": "Notify on join"}},
                {"type": "input", "block_id": "dm_message",
                 "element": {"type": "plain_text_input", "action_id": "val", "initial_value": (s.dm_message if s and s.dm_message else "")},
                 "label": {"type": "plain_text", "text": "DM message"}},
            ],
        }
        await client.views_open(trigger_id=trigger_id, view=view)

    @reg.interactions.view_submission("admin_settings")
    async def admin_settings_submit(payload: Dict[str, Any]) -> None:
        state = payload.get("view", {}).get("state", {}).get("values", {})
        def _conv(block_id: str) -> Optional[str]:
            try:
                return state[block_id]["val"]["selected_conversation"]
            except Exception:
                return None
        def _sel(block_id: str) -> Optional[bool]:
            try:
                v = state[block_id]["val"]["selected_option"]["value"]
                return v == "on"
            except Exception:
                return None
        def _text(block_id: str) -> Optional[str]:
            try:
                return state[block_id]["val"]["value"]
            except Exception:
                return None

        admin_channel = _conv("admin_channel")
        audit_channel = _conv("audit_channel")
        notify = _sel("notify")
        dm_message = _text("dm_message")

        ctx = get_context()
        repo = InviteSettingsRepository(ctx.engine)
        await repo.upsert(admin_channel_id=admin_channel, audit_channel_id=audit_channel, notify_on_join=notify, dm_message=dm_message)

