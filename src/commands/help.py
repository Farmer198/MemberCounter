import discord

from discord.ext import commands
from discord import app_commands

from MemberCounter import MemberCounter

async def setup(bot):
    await bot.add_cog(help(bot))

class help(commands.Cog):
    def __init__(self, bot: MemberCounter):
        self.bot: MemberCounter = bot

    @app_commands.command(
        name = "help",
        description = "Shows all commands."
    )
    @app_commands.checks.bot_has_permissions(send_messages = True, read_messages = True, embed_links = True)
    @app_commands.guild_only()
    async def _help(self, interaction: discord.Interaction):
        cmds = await self.bot.tree.fetch_commands()
        description = [f"{command.mention}: {command.description}" for command in cmds]

        embed = discord.Embed(
            color = self.bot.color,
            description = "\n".join(description)
        )
        embed.set_author(name = self.bot.user.name, icon_url = self.bot.user.avatar)

        return await interaction.response.send_message(embed = embed, ephemeral = True)
