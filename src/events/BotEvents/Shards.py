from __future__ import annotations

from typing import TYPE_CHECKING
from discord.ext.commands import Cog

__all__ = (
    'Shards'
)

if TYPE_CHECKING:
    from MemberCounter import MemberCounter

async def setup(bot: MemberCounter):
    await bot.add_cog(Shards(bot))


class Shards(Cog):
    def __init__(self, bot: MemberCounter) -> None:
        self.bot: MemberCounter = bot

    async def on_shard_ready(self, shard_id) -> None:
        self.bot.logger.info(f'Shard Ready {shard_id + 1}\{self.bot.shard_count}')

    async def on_shard_resumed(self, shard_id) -> None:
        self.bot.logger.info(f'Shard resumed {shard_id + 1}\{self.bot.shard_count}')

    async def on_shard_connect(self, shard_id) -> None:
        self.bot.logger.info(f'Shard Connected {shard_id + 1}\{self.bot.shard_count}')

    async def on_shard_disconnect(self, shard_id) -> None:
        self.bot.logger.info(f'Shard Disconnected {shard_id + 1}\{self.bot.shard_count}')
