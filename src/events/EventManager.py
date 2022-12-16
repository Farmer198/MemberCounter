from .EventManagerBlueprint import EventManagerBlueprint
from .events import (
    CommandError,
    GuildJoin,
    GuildRemove,
    MemberJoin,
    MemberRemove,
    Shards
)

class EventManager(EventManagerBlueprint):
    def __init__(self, client) -> None:
        self.client = client
        self.events = []

    def start(self):
        self.register()
        self.load()

    def register(self):
        self.events.append(CommandError(self))
        self.events.append(GuildJoin(self))
        self.events.append(GuildRemove(self))
        self.events.append(MemberJoin(self))
        self.events.append(MemberRemove(self))
        self.events.append(Shards(self))

    def load(self):
        [event.load() for event in self.events]
