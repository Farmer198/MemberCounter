import discord

from discord import app_commands
from discord.ext import commands
from MemberCounter import MemberCounter

async def setup(bot):
    await bot.add_cog(uptime(bot))

class uptime(commands.Cog):
    def __init__(self, bot: MemberCounter):
        self.bot: MemberCounter = bot

    @app_commands.command(
        name = 'uptime',
        description = "Shows the bots uptime."
    )
    @app_commands.checks.bot_has_permissions(send_messages = True, read_messages = True, embed_links = True)
    @app_commands.guild_only()
    async def _uptime(self, interaction: discord.Interaction):

        # Uptime
        m, s = divmod(self.bot.uptimer.uptime, 60)
        h, m = divmod(m, 60)
        d, h = divmod(h, 24)
        j, d = divmod(d, 365)
        if d:
            time = '%sd %sh %sm %ss' % (d, h, m, s)
        else:
            time = '%sh %sm %ss' % (h, m, s)

        embed = discord.Embed(
            color = self.bot.color,
            description = time
        )

        return await interaction.response.send_message(embed = embed, ephemeral = True)
