from __future__ import annotations

from typing import TYPE_CHECKING
from discord import Interaction
from discord.ext.commands import Cog
from discord.app_commands import AppCommandError
from discord.app_commands.errors import (
    AppCommandError,
    CommandNotFound
)

__all__ = (
    'CommandError'
)

if TYPE_CHECKING:
    from MemberCounter import MemberCounter

async def setup(bot: MemberCounter):
    await bot.add_cog(CommandError(bot))

class CommandError(Cog):
    def __init__(self, bot: MemberCounter) -> None:
        self.bot: MemberCounter = bot

    @Cog.listener()
    async def on_app_command_error(self, interaction: Interaction, error: AppCommandError) -> None:
        if isinstance(error, CommandNotFound):
            try:
                return await interaction.response.defer()
            except:
                return

        self.bot.logger.error("[AppCommand] {} - {} | {} ({})\n{}".format(interaction.command.name, interaction.user, interaction.guild.name, interaction.guild_id, error))
