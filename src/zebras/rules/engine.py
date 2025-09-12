from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional


class Decision(Enum):
    ALLOW = "allow"
    DENY = "deny"
    NEUTRAL = "neutral"


@dataclass
class Result:
    decision: Decision
    reason: Optional[str] = None


class Rule:
    async def evaluate(self, context: Dict[str, Any], event: Dict[str, Any]) -> Result:  # noqa: D401
        """Return a decision for the event."""
        return Result(Decision.NEUTRAL)


class Engine:
    def __init__(self) -> None:
        self._rules: List[Rule] = []

    def add(self, rule: Rule) -> None:
        self._rules.append(rule)

    async def evaluate(self, context: Dict[str, Any], event: Dict[str, Any]) -> Result:
        final = Result(Decision.NEUTRAL)
        for rule in self._rules:
            r = await rule.evaluate(context, event)
            if r.decision == Decision.DENY:
                return r
            if r.decision == Decision.ALLOW:
                final = r
        return final

