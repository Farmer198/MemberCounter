from __future__ import annotations

from typing import TYPE_CHECKING, List
from .EventManagerBlueprint import EventManagerBlueprint
from .events import (
    CommandError,
    GuildJoin,
    GuildRemove,
    MemberJoin,
    MemberRemove,
    Shards
)

__all__ = (
    'EventManager'
)

if TYPE_CHECKING:
    from MemberCounter import MemberCounter

class EventManager(EventManagerBlueprint):
    def __init__(self, client: MemberCounter) -> None:
        self.client: MemberCounter = client
        self.events: List = []

    def start(self) -> None:
        self.register()
        self.load()

    def register(self) -> None:
        self.events.append(CommandError(self))
        self.events.append(GuildJoin(self))
        self.events.append(GuildRemove(self))
        self.events.append(MemberJoin(self))
        self.events.append(MemberRemove(self))
        self.events.append(Shards(self))

    def load(self) -> None:
        [event.load() for event in self.events]
