from discord import Guild
from ..EventManagerBlueprint import EventBlueprint

class GuildJoin(EventBlueprint):
    def __init__(self, manager) -> None:
        self.manager = manager

    def load(self):
        self.manager.client.add_listener(self.on_guild_join)

    def unload(self):
        self.manager.client.remove_listener(self.on_guild_join)

    async def on_guild_join(self, guild: Guild):
        self.manager.client.logger.info(f"Guild Joined [ID: {guild.id}]")
        await self.manager.client.updater.update_counter(guild.id)
