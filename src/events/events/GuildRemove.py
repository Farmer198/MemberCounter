from discord import Guild
from ..EventManagerBlueprint import EventBlueprint

class GuildRemove(EventBlueprint):
    def __init__(self, manager) -> None:
        self.manager = manager

    def load(self):
        self.manager.client.add_listener(self.on_guild_remove)

    def unload(self):
        self.manager.client.remove_listener(self.on_guild_remove)

    async def on_guild_remove(self, guild: Guild):
        self.manager.client.logger.info(f"Guild Removed [ID: {guild.id}]")
        self.manager.client.servers.delete_server(guild.id)
