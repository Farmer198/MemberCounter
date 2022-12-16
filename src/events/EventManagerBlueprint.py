from typing import List
from discord import Client
from .Exeptions import NotImplementedError

class EventManagerBlueprint:
    client: Client
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
