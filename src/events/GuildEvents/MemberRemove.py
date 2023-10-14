from __future__ import annotations

from typing import TYPE_CHECKING
from discord import RawMemberRemoveEvent
from discord.ext.commands import Cog

__all__ = (
    'MemberRemove'
)

if TYPE_CHECKING:
    from MemberCounter import MemberCounter

async def setup(bot: MemberCounter):
    await bot.add_cog(MemberRemove(bot))


class MemberRemove(Cog):
    def __init__(self, bot: MemberCounter) -> None:
        self.bot: MemberCounter = bot

    async def on_raw_member_remove(self, payload: RawMemberRemoveEvent) -> None:
        if payload.user.id == self.bot.user.id:
            return
        await self.bot.updater.update_counter(payload.guild_id)
