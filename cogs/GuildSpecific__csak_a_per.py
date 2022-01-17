import discord
from discord.ext import commands


class GuildSpecific__csak_a_per(commands.Cog):
    def __init__(self, client):
        self.client = client
        print('Loaded', __name__)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id != 920590116710412298 or message.author == self.client.user:
            return
        if message.attachments == []:
            await message.channel.send("Ide csak a shopodat küldjed. Kell lennie egy fényképnek csatolva.", delete_after=10)
            return await message.delete()
        name = f"{message.author.name}`s shop"
        to_delete = [
            thread for thread in message.channel.threads if thread.name == name and not thread.archived]
        for t in to_delete:
            await t.archive()
        await message.channel.create_thread(name=name, message=message)


def setup(client):
    client.add_cog(GuildSpecific__csak_a_per(client))
