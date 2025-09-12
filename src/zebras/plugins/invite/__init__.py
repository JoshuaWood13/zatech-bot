from __future__ import annotations

from typing import Any, Dict, Optional
from datetime import datetime

from slack_sdk.web.async_client import AsyncWebClient

from ...plugin import Registry
from ...app_context import get_context
from .repository import InviteSettingsRepository


async def _client() -> AsyncWebClient:
    ctx = get_context()
    return await ctx.web_client()


def register(reg: Registry) -> None:
    @reg.commands.slash("/invite-helper")
    async def invite_cmd(payload: Dict[str, Any]) -> Dict[str, Any]:
        text = (payload.get("text") or "").strip()
        ctx = get_context()
        repo = InviteSettingsRepository(ctx.engine)
        channel_id = payload.get("channel_id")

        if text.startswith("set-channel "):
            # expects <#CXXXX|name> or CXXXX
            arg = text.split(" ", 1)[1]
            ch = arg.strip("<>")
            if ch.startswith("#") and "|" in ch:
                ch = ch[1:].split("|", 1)[0]
            await repo.upsert(admin_channel_id=ch)
            return {"response_type": "ephemeral", "text": f"Admin channel set to <#{ch}>"}

        if text.startswith("notify "):
            val = text.split(" ", 1)[1].lower() in ("on", "true", "yes")
            await repo.upsert(notify_on_join=val)
            return {"response_type": "ephemeral", "text": f"Notify on join {'ON' if val else 'OFF'}"}

        if text.startswith("message "):
            msg = text.split(" ", 1)[1]
            await repo.upsert(dm_message=msg)
            return {"response_type": "ephemeral", "text": "Updated DM message template."}

        s = await repo.get()
        return {
            "response_type": "ephemeral",
            "text": (
                "Invite Helper settings:\n"
                f"- Admin channel: <#{(s.admin_channel_id if s else 'unset')}>\n"
                f"- Notify on join: {('ON' if (s and s.notify_on_join) else 'OFF')}\n"
                "\nCommands:\n"
                "- /invite-helper set-channel #channel\n"
                "- /invite-helper notify on|off\n"
                "- /invite-helper message <text>\n"
            ),
        }

    @reg.events.on("team_join")
    async def on_team_join(payload: Dict[str, Any]) -> None:
        ctx = get_context()
        repo = InviteSettingsRepository(ctx.engine)
        s = await repo.get()
        if not s:
            return
        client = await _client()
        user = payload.get("event", {}).get("user", {})
        user_id = user.get("id") if isinstance(user, dict) else None

        # Notify admins
        if s.notify_on_join and s.admin_channel_id:
            try:
                await client.chat_postMessage(
                    channel=s.admin_channel_id,
                    text=f"New member joined: <@{user_id}>",
                )
            except Exception:
                pass

        # DM onboarding message
        if s.dm_message and user_id:
            try:
                resp = await client.conversations_open(users=user_id)
                dm = resp.get("channel", {}).get("id")
                if dm:
                    await client.chat_postMessage(channel=dm, text=s.dm_message)
            except Exception:
                pass

