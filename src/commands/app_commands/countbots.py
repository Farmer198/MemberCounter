from __future__ import annotations

import discord

from discord import app_commands
from discord.ext import commands
from typing import TYPE_CHECKING, Optional

__all__ = (
    'countbots'
)

if TYPE_CHECKING:
    from MemberCounter import MemberCounter

async def setup(bot: MemberCounter):
    await bot.add_cog(countbots(bot))

class countbots(commands.Cog):
    def __init__(self, bot: MemberCounter):
        self.bot: MemberCounter = bot

    @app_commands.command(
        name = 'countbots',
        description = "Shows whether bots are also counted."
    )
    @app_commands.checks.bot_has_permissions(send_messages = True, read_messages = True, embed_links = True)
    @app_commands.default_permissions(administrator = True)
    @app_commands.describe(value = "Specify whether bots are also counted.")
    @app_commands.guild_only()
    async def _countbots(self, interaction: discord.Interaction, value: Optional[bool]):
        server = self.bot.servers.get_server(interaction.guild_id)

        if value is not None:
            server.set_count_bots(value)
            await self.bot.updater.update_counter(interaction.guild_id) 
            if value:
                embed = discord.Embed(
                    color = self.bot.color,
                    description = "Bots are also counted from now on."
                )
            else:
                embed = discord.Embed(
                    color = self.bot.color,
                    description = "Bots will not be counted as of now."
                )
        else:
            if server.count_bots:
                embed = discord.Embed(
                    color = self.bot.color,
                    description = "Bots are counted."
                )
            else:
                embed = discord.Embed(
                    color = self.bot.color,
                    description = "Bots are not counted."
                )
        return await interaction.response.send_message(embed = embed, ephemeral = True)
