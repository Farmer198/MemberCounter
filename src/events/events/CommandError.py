from discord import Interaction
from discord.app_commands import AppCommandError
from discord.app_commands.errors import (
    AppCommandError,
    CommandNotFound
)
from ..EventManagerBlueprint import EventBlueprint

class CommandError(EventBlueprint):
    def __init__(self, manager) -> None:
        self.manager = manager

    def load(self):
        self.manager.client.add_listener(self.on_app_command_error)

    def unload(self):
        self.manager.client.remove_listener(self.on_app_command_error)

    async def on_app_command_error(self, interaction: Interaction, error: AppCommandError):
        if isinstance(error, CommandNotFound):
            try:
                return await interaction.response.defer()
            except:
                return

        interaction.client.logger.error("[AppCommand] {} - {} | {} ({})\n{}".format(interaction.command.name, interaction.user, interaction.guild.name, interaction.guild_id, error))
