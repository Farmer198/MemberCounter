import discord

permission = discord.Permissions()

permission.administrator = True

permission.change_nickname = True
permission.send_messages = True
permission.embed_links = True

print(permission.value)