from __future__ import annotations

import hmac
import hashlib
import logging
import time
from typing import Any, Dict

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, PlainTextResponse
from starlette.datastructures import FormData
import json

from ..router import Router
from ..plugin.registry import Registry


log = logging.getLogger("zebras.http")


def verify_slack_signature(req: Request, signing_secret: str, body: bytes) -> None:
    ts = req.headers.get("X-Slack-Request-Timestamp")
    sig = req.headers.get("X-Slack-Signature")
    if not ts or not sig:
        raise HTTPException(status_code=401, detail="Missing Slack signature")
    if abs(time.time() - int(ts)) > 60 * 5:
        raise HTTPException(status_code=401, detail="Stale request")
    base = f"v0:{ts}:{body.decode()}".encode()
    digest = hmac.new(signing_secret.encode(), base, hashlib.sha256).hexdigest()
    expected = f"v0={digest}"
    if not hmac.compare_digest(expected, sig):
        raise HTTPException(status_code=401, detail="Invalid signature")


def create_app(router: Router, signing_secret: str | None, registry: Registry) -> FastAPI:
    app = FastAPI()

    @app.get("/healthz")
    async def healthz() -> Dict[str, str]:
        return {"status": "ok"}

    @app.post("/slack/events")
    async def slack_events(request: Request) -> Any:
        body = await request.body()
        if signing_secret:
            verify_slack_signature(request, signing_secret, body)

        payload = await request.json()
        # URL verification challenge
        if payload.get("type") == "url_verification":
            return PlainTextResponse(payload.get("challenge", ""))

        await router.dispatch(payload)
        return JSONResponse({"ok": True})

    @app.post("/slack/commands")
    async def slack_commands(request: Request) -> Any:
        body = await request.body()
        if signing_secret:
            verify_slack_signature(request, signing_secret, body)
        # Slack sends application/x-www-form-urlencoded
        form: FormData = await request.form()
        data = {k: form.get(k) for k in form.keys()}
        cmd = data.get("command")
        if not cmd:
            return JSONResponse({"error": "missing command"}, status_code=400)
        handler = registry.slash_commands.get(cmd)
        if not handler:
            return JSONResponse({"response_type": "ephemeral", "text": f"Unknown command: {cmd}"})
        try:
            result = await handler(data)
        except Exception:
            log.exception("Slash command handler error for %s", cmd)
            result = {"response_type": "ephemeral", "text": "An error occurred."}
        # Immediate response body is accepted by Slack for slash commands
        if result is None:
            result = {"response_type": "ephemeral", "text": "OK"}
        return JSONResponse(result)

    @app.post("/slack/interactivity")
    async def slack_interactivity(request: Request) -> Any:
        body = await request.body()
        if signing_secret:
            verify_slack_signature(request, signing_secret, body)
        form: FormData = await request.form()
        payload_raw = form.get("payload")
        if not payload_raw:
            return JSONResponse({"error": "missing payload"}, status_code=400)
        try:
            payload = json.loads(payload_raw)
        except Exception:
            return JSONResponse({"error": "invalid payload"}, status_code=400)
        t = payload.get("type")
        if t == "block_actions":
            action = (payload.get("actions") or [{}])[0]
            cb = action.get("action_id") or action.get("callback_id") or payload.get("callback_id")
            handler = registry.actions.get(cb)
            if handler:
                await handler(payload)
            return JSONResponse({"ok": True})
        if t == "view_submission":
            cb = payload.get("view", {}).get("callback_id")
            handler = registry.views.get(cb)
            if handler:
                await handler(payload)
            return JSONResponse({"response_action": "clear"})
        return JSONResponse({"ok": True})

    return app
