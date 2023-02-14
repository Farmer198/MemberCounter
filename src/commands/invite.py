from __future__ import annotations

import discord

from discord import app_commands
from discord.ext import commands
from typing import TYPE_CHECKING

__all__ = (
    'invite'
)

if TYPE_CHECKING:
    from MemberCounter import MemberCounter

async def setup(bot: MemberCounter):
    await bot.add_cog(invite(bot))

class invite(commands.Cog):
    def __init__(self, bot: MemberCounter):
        self.bot: MemberCounter = bot

    @app_commands.command(
        name = 'invite',
        description = "Add the bot to another server."
    )
    @app_commands.checks.bot_has_permissions(send_messages = True, read_messages = True, embed_links = True)
    @app_commands.guild_only()
    async def _invite(self, interaction: discord.Interaction):        
        embed = discord.Embed(
            color = self.bot.color,
            description = "[Click here]({}) to invite the bot.".format(self.bot.invite_url)
        )
        return await interaction.response.send_message(embed = embed, ephemeral = True)
