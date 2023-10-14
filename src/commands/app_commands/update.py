from __future__ import annotations

import discord

from discord import app_commands
from discord.ext import commands
from typing import TYPE_CHECKING

__all__ = (
    'update'
)

if TYPE_CHECKING:
    from MemberCounter import MemberCounter

async def setup(bot: MemberCounter):
    await bot.add_cog(update(bot))

class update(commands.Cog):
    def __init__(self, bot: MemberCounter):
        self.bot: MemberCounter = bot

    @app_commands.command(
        name = 'update',
        description = "Use this command to update the nickname when the amount isn't correct."
    )
    @app_commands.checks.bot_has_permissions(send_messages = True, read_messages = True, embed_links = True)
    @app_commands.default_permissions(administrator = True)
    @app_commands.guild_only()
    async def _update(self, interaction: discord.Interaction):
        await self.bot.updater.update_counter(interaction.guild_id)                
        embed = discord.Embed(
            color = self.bot.color,
            description = "Counter updated!"
        )
        return await interaction.response.send_message(embed = embed, ephemeral = True)
