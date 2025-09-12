from __future__ import annotations

from typing import Any, Awaitable, Callable, Dict, List, Optional
import logging


Handler = Callable[..., Awaitable[None]]


class Registry:
    """Collects plugin handlers and registers them with the router/adapter.

    This is a minimal placeholder: it stores handlers in maps that the app core
    can bind to the Router and Slack adapters.
    """

    def __init__(self) -> None:
        self.log = logging.getLogger("zebras.plugin.registry")
        self.event_handlers: Dict[str, List[Handler]] = {}
        self.slash_commands: Dict[str, Handler] = {}
        self.actions: Dict[str, Handler] = {}
        self.views: Dict[str, Handler] = {}

    class _Events:
        def __init__(self, outer: "Registry") -> None:
            self._outer = outer

        def on(self, event_type: str, **filters: Any):  # noqa: ARG002
            def decorator(fn: Handler) -> Handler:
                self._outer.event_handlers.setdefault(event_type, []).append(fn)
                return fn

            return decorator

    class _Commands:
        def __init__(self, outer: "Registry") -> None:
            self._outer = outer

        def slash(self, name: str):
            def decorator(fn: Handler) -> Handler:
                self._outer.slash_commands[name] = fn
                return fn

            return decorator

    class _Actions:
        def __init__(self, outer: "Registry") -> None:
            self._outer = outer

        def action(self, callback_id: str):
            def decorator(fn: Handler) -> Handler:
                self._outer.actions[callback_id] = fn
                return fn

            return decorator

        def view_submission(self, callback_id: str):
            def decorator(fn: Handler) -> Handler:
                self._outer.views[callback_id] = fn
                return fn

            return decorator

    @property
    def events(self) -> "Registry._Events":
        return Registry._Events(self)

    @property
    def commands(self) -> "Registry._Commands":
        return Registry._Commands(self)

    @property
    def interactions(self) -> "Registry._Actions":
        return Registry._Actions(self)

