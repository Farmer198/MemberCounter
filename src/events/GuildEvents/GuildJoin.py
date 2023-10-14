from __future__ import annotations

from typing import TYPE_CHECKING
from discord import Guild
from discord.ext.commands import Cog

__all__ = (
    'GuildJoin'
)

if TYPE_CHECKING:
    from MemberCounter import MemberCounter

async def setup(bot: MemberCounter):
    await bot.add_cog(GuildJoin(bot))


class GuildJoin(Cog):
    def __init__(self, bot: MemberCounter) -> None:
        self.bot: MemberCounter = bot

    async def on_guild_join(self, guild: Guild) -> None:
        self.bot.logger.info(f"Guild Joined [ID: {guild.id}]")
        await self.bot.updater.update_counter(guild.id)
