from __future__ import annotations

import asyncio
import logging
from typing import Any, Dict

from slack_sdk.web.async_client import AsyncWebClient
from slack_sdk.socket_mode.aiohttp import SocketModeClient
from slack_sdk.socket_mode.request import SocketModeRequest
from slack_sdk.socket_mode.response import SocketModeResponse

from ..router import Router
from ..plugin.registry import Registry
import aiohttp


class SocketApp:
    def __init__(self, bot_token: str, app_token: str, router: Router, registry: Registry) -> None:
        self.log = logging.getLogger("zebras.slack.socket")
        self._bot_token = bot_token
        self._app_token = app_token
        self.client: AsyncWebClient | None = None
        self.socket: SocketModeClient | None = None
        self.router = router
        self.registry = registry

    async def _on_event(self, client: SocketModeClient, req: SocketModeRequest) -> None:  # noqa: ARG002
        if req.type == "events_api":
            # Acknowledge first
            assert self.socket is not None
            await self.socket.send_socket_mode_response(SocketModeResponse(envelope_id=req.envelope_id))
            await self.router.dispatch(req.payload)
        elif req.type == "slash_commands":
            # Acknowledge first
            assert self.socket is not None
            await self.socket.send_socket_mode_response(SocketModeResponse(envelope_id=req.envelope_id))
            payload = req.payload  # form fields as dict
            cmd = payload.get("command")
            if not cmd:
                return
            handler = self.registry.slash_commands.get(cmd)
            if not handler:
                self.log.debug("No handler for command %s", cmd)
                return
            try:
                result = await handler(payload)
            except Exception:
                self.log.exception("Slash command handler error for %s", cmd)
                result = {"response_type": "ephemeral", "text": "An error occurred."}

            # Respond via response_url if available
            response_url = payload.get("response_url")
            if response_url and result:
                async with aiohttp.ClientSession() as session:
                    await session.post(response_url, json=result)

    async def run(self) -> None:
        # Lazily create clients after loop is running
        self.client = AsyncWebClient(token=self._bot_token)
        self.socket = SocketModeClient(app_token=self._app_token, web_client=self.client)
        self.socket.socket_mode_request_listeners.append(self._on_event)
        await self.socket.connect()
        self.log.info("Socket Mode connected")
        # Keep alive
        while True:
            await asyncio.sleep(3600)
