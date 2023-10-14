from __future__ import annotations

from typing import TYPE_CHECKING
from discord import Member
from discord.ext.commands import Cog

__all__ = (
    'MemberJoin'
)

if TYPE_CHECKING:
    from MemberCounter import MemberCounter

async def setup(bot: MemberCounter):
    await bot.add_cog(MemberJoin(bot))


class MemberJoin(Cog):
    def __init__(self, bot: MemberCounter) -> None:
        self.bot: MemberCounter = bot

    async def on_member_join(self, member: Member) -> None:
        await self.bot.updater.update_counter(member.guild.id)
   