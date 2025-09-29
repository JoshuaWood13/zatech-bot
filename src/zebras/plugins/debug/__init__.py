from __future__ import annotations

import asyncio
from typing import Any, Dict

from sqlalchemy import text
from slack_sdk.web.async_client import AsyncWebClient

from ...plugin import Registry
from ...app_context import get_context


async def _client() -> AsyncWebClient:
    return await get_context().web_client()


def register(reg: Registry) -> None:
    @reg.commands.slash("/debug")
    async def debug_cmd(payload: Dict[str, Any]) -> Dict[str, Any]:
        ctx = get_context()
        results: list[str] = []

        # Slack auth check
        try:
            client = await _client()
            auth = await client.auth_test()
            team = auth.get("team") or auth.get("team_id")
            user = auth.get("user_id") or auth.get("user")
            results.append(f"slack: ok (team={team}, bot_user={user})")
        except Exception as e:  # pragma: no cover - best-effort debug
            results.append(f"slack: ERROR ({e.__class__.__name__}: {e})")

        # Database check
        try:
            async with ctx.engine.connect() as conn:
                await conn.execute(text("select 1"))
            results.append("db: ok")
        except Exception as e:  # pragma: no cover
            results.append(f"db: ERROR ({e.__class__.__name__}: {e})")

        # Redis check (sync client; run in executor)
        try:
            loop = asyncio.get_running_loop()
            pong = await loop.run_in_executor(None, ctx.redis.ping)
            results.append("redis: ok" if pong else "redis: ERROR (no PONG)")
        except Exception as e:  # pragma: no cover
            results.append(f"redis: ERROR ({e.__class__.__name__}: {e})")

        # Commands registered
        try:
            cmds = ", ".join(sorted(reg.slash_commands.keys()))
            results.append(f"commands: {cmds}")
        except Exception:
            pass

        text_out = "*ZEBRAS Debug*\n" + "\n".join(f"• {line}" for line in results)
        return {"response_type": "ephemeral", "text": text_out}

