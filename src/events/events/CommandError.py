from __future__ import annotations

from typing import TYPE_CHECKING
from discord import Interaction
from discord.app_commands import AppCommandError
from discord.app_commands.errors import (
    AppCommandError,
    CommandNotFound
)
from ..EventManagerBlueprint import EventBlueprint

__all__ = (
    'CommandError'
)

if TYPE_CHECKING:
    from ..EventManager import EventManager

class CommandError(EventBlueprint):
    def __init__(self, manager: EventManager) -> None:
        self.manager: EventManager = manager

    def load(self) -> None:
        self.manager.client.add_listener(self.on_app_command_error)

    def unload(self) -> None:
        self.manager.client.remove_listener(self.on_app_command_error)

    async def on_app_command_error(self, interaction: Interaction, error: AppCommandError) -> None:
        if isinstance(error, CommandNotFound):
            try:
                return await interaction.response.defer()
            except:
                return

        interaction.client.logger.error("[AppCommand] {} - {} | {} ({})\n{}".format(interaction.command.name, interaction.user, interaction.guild.name, interaction.guild_id, error))
