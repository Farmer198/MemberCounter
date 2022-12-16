from discord import RawMemberRemoveEvent
from ..EventManagerBlueprint import EventBlueprint

class MemberRemove(EventBlueprint):
    def __init__(self, manager) -> None:
        self.manager = manager

    def load(self):
        self.manager.client.add_listener(self.on_raw_member_remove)

    def unload(self):
        self.manager.client.remove_listener(self.on_raw_member_remove)

    async def on_raw_member_remove(self, payload: RawMemberRemoveEvent):
        if payload.user.id == self.manager.client.user.id:
            return
        await self.manager.client.updater.update_counter(payload.guild_id)
