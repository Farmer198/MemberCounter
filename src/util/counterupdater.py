from discord import Guild
from time import time

class CounterUpdater:
    def __init__(self, client) -> None:
        self.client = client

    async def update_counter(self, guild_id: int):

        guild: Guild = self.client.get_guild(guild_id)
        server = self.client.servers.get_server(guild_id)

        if guild is None:
            return

        # if the guild has more than 1000 members, it can be updated only 10min after the last update 
        if guild.member_count > 1000 and int(time() - server.last_update) < 600:
            return

        count = guild.member_count
        if not server.count_bots:
            count = len([member for member in guild.members if not member.bot])

        if guild.me.guild_permissions.change_nickname:
            server.set_last_update(int(time()))
            try:
                await guild.me.edit(nick = "Members: {}".format(self.format_count(count)))
            except:
                pass

    def format_count(self, count: int) -> str:
        if count < 1000:
            return f"{count}"
        else:
            return f"{round(count / 1000, 1)}K"
