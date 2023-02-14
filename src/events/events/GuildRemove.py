from __future__ import annotations

from typing import TYPE_CHECKING
from discord import Guild
from ..EventManagerBlueprint import EventBlueprint

__all__ = (
    'GuildRemove'
)

if TYPE_CHECKING:
    from ..EventManager import EventManager

class GuildRemove(EventBlueprint):
    def __init__(self, manager: EventManager) -> None:
        self.manager: EventManager = manager

    def load(self) -> None:
        self.manager.client.add_listener(self.on_guild_remove)

    def unload(self) -> None:
        self.manager.client.remove_listener(self.on_guild_remove)

    async def on_guild_remove(self, guild: Guild) -> None:
        self.manager.client.logger.info(f"Guild Removed [ID: {guild.id}]")
        self.manager.client.servers.delete_server(guild.id)
