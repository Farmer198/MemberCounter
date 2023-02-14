from __future__ import annotations

from typing import TYPE_CHECKING
from discord import RawMemberRemoveEvent
from ..EventManagerBlueprint import EventBlueprint

__all__ = (
    'MemberRemove'
)

if TYPE_CHECKING:
    from ..EventManager import EventManager

class MemberRemove(EventBlueprint):
    def __init__(self, manager: EventManager) -> None:
        self.manager: EventManager = manager

    def load(self) -> None:
        self.manager.client.add_listener(self.on_raw_member_remove)

    def unload(self) -> None:
        self.manager.client.remove_listener(self.on_raw_member_remove)

    async def on_raw_member_remove(self, payload: RawMemberRemoveEvent) -> None:
        if payload.user.id == self.manager.client.user.id:
            return
        await self.manager.client.updater.update_counter(payload.guild_id)
