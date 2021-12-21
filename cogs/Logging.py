from discord.ext import commands
from datetime import datetime
from time import time
import json
import asyncio
import aiohttp
import atexit


class Logging(commands.Cog):
    def __init__(self, client):
        self.client = client
        print(f'Loaded', __name__)

    """async def uptime_log(self):
        while True:
            with open("./data/uptime_ping.json", "w") as file:
                json.dump({"last_up": time()}, file)

            await asyncio.sleep(10)"""

    """ @atexit.register
    async def last_up():
        print(time())  # TODO Send message + read when stattded """

    @commands.Cog.listener()
    async def on_ready(self):
        self.client.logging_channel = self.client.get_channel(
            self.client.data["logging"]["channel"])
        self.client.logging_message = await self.client.logging_channel.fetch_message(
            self.client.data["logging"]["message"])
        self.client.last_up = float(self.client.logging_message.content)
        await self.client.logging_channel.send(f"**The bot is back online, after being offline for ~`{round(time() - self.client.last_up)}` seconds.**")
        while True:
            await asyncio.sleep(10)
            await self.client.logging_message.edit(content=str(time()))

    @commands.Cog.listener()
    async def on_command(self, ctx):
        guild = ctx.guild.name
        author = f"{ctx.author.name}#{ctx.author.discriminator}"
        channel = ctx.channel.name
        command = ctx.message.content.replace(self.client.prefix, "")
        log = f"**{guild}:** *{author}* invoked `{command}` in `#{channel}`"
        await self.client.logging_channel.send(log)


def setup(client):
    client.add_cog(Logging(client))
