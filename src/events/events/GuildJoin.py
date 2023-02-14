from __future__ import annotations

from typing import TYPE_CHECKING
from discord import Guild
from ..EventManagerBlueprint import EventBlueprint

__all__ = (
    'GuildJoin'
)

if TYPE_CHECKING:
    from ..EventManager import EventManager

class GuildJoin(EventBlueprint):
    def __init__(self, manager: EventManager) -> None:
        self.manager: EventManager = manager

    def load(self) -> None:
        self.manager.client.add_listener(self.on_guild_join)

    def unload(self) -> None:
        self.manager.client.remove_listener(self.on_guild_join)

    async def on_guild_join(self, guild: Guild) -> None:
        self.manager.client.logger.info(f"Guild Joined [ID: {guild.id}]")
        await self.manager.client.updater.update_counter(guild.id)
