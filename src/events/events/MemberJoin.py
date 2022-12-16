from discord import Member
from ..EventManagerBlueprint import EventBlueprint

class MemberJoin(EventBlueprint):
    def __init__(self, manager) -> None:
        self.manager = manager

    def load(self):
        self.manager.client.add_listener(self.on_member_join)

    def unload(self):
        self.manager.client.remove_listener(self.on_member_join)

    async def on_member_join(self, member: Member):
        await self.manager.client.updater.update_counter(member.guild.id)
   