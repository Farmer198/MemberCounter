from __future__ import annotations

from typing import TYPE_CHECKING
from discord import Member
from ..EventManagerBlueprint import EventBlueprint

__all__ = (
    'MemberJoin'
)

if TYPE_CHECKING:
    from ..EventManager import EventManager

class MemberJoin(EventBlueprint):
    def __init__(self, manager: EventManager) -> None:
        self.manager: EventManager = manager

    def load(self) -> None:
        self.manager.client.add_listener(self.on_member_join)

    def unload(self) -> None:
        self.manager.client.remove_listener(self.on_member_join)

    async def on_member_join(self, member: Member) -> None:
        await self.manager.client.updater.update_counter(member.guild.id)
   