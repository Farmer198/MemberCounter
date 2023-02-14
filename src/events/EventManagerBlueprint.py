from __future__ import annotations

from typing import TYPE_CHECKING, List
from .Exeptions import NotImplementedError

__all__ = (
    'EventManagerBlueprint',
    'EventBlueprint'
)

if TYPE_CHECKING:
    from MemberCounter import MemberCounter

class EventManagerBlueprint:
    client: MemberCounter
    events: List

class EventBlueprint:
    manager: EventManagerBlueprint

    def load(self):
        """
        To load the Event.
        """
        raise NotImplementedError

    def unload(self):
        """
        To unload the Event.
        """
        raise NotImplementedError
