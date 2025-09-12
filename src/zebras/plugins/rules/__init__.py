from __future__ import annotations

from typing import Dict, Any

from ...plugin import Registry


def register(reg: Registry) -> None:
    @reg.commands.slash("/rules")
    async def rules_cmd(payload: Dict[str, Any]) -> Dict[str, Any]:
        text = (payload.get("text") or "").strip()
        if not text or text == "help":
            return {
                "response_type": "ephemeral",
                "text": "Rules: list | enable <rule> | disable <rule> (stub)",
            }
        if text == "list":
            return {"response_type": "ephemeral", "text": "No rules defined yet."}
        return {"response_type": "ephemeral", "text": f"Unrecognized: {text}"}

