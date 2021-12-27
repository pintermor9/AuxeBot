import discord
from discord.ext import commands
import json


class Poll(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        self.client.poll_channel = self.client.get_channel(
            self.client.data["poll"]["channel"])
        self.client.poll_message = await self.client.poll_channel.fetch_message(
            self.client.data["poll"]["message"])
        self.client.poll_data = json.loads(
            self.client.poll_message.content)
        print(__name__+": "+str(self.client.poll_data))


def setup(client):
    client.add_cog(Poll(client))
