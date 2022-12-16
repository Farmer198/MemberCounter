import discord

permission = discord.Permissions()

permission.change_nickname = True
permission.send_messages = True

print(permission.value)