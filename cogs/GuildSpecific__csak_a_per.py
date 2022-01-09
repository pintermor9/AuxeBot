import discord
from discord.ext import commands


class GuildSpecific__csak_a_per(commands.Cog):
    def __init__(self, client):
        self.client = client
        print('Loaded', __name__)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id != 920590116710412298:
            return
        if message.attachments == []:
            return await message.delete()
        await message.channel.create_thread(name=f"{message.author.name}`s shop", message=message)


def setup(client):
    client.add_cog(GuildSpecific__csak_a_per(client))
