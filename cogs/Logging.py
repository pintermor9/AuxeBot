from discord.ext import commands
from datetime import timedelta
from time import time
import json
import asyncio
import aiohttp
import atexit


class Logging(commands.Cog):
    def __init__(self, client):
        self.client = client
        print(f'Loaded', __name__)

    @commands.Cog.listener()
    async def on_ready(self):
        self.client.logging_channel = self.client.get_channel(
            self.client.data["logging"]["channel"])
        self.client.logging_message = await self.client.logging_channel.fetch_message(
            self.client.data["logging"]["message"])
        self.client.last_up = float(self.client.logging_message.content)
        hours, minutes, seconds = str(timedelta(
            seconds=round(time() - self.client.last_up))).split(":")
        await self.client.logging_channel.send(f"**The bot is back online, after being offline for ~`{hours} hour(s), {minutes} minute(s), {seconds} second(s)`.**")
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
