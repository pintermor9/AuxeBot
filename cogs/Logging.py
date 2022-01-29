from discord.ext import commands
from datetime import timedelta
from time import time
import asyncio


class Logging(commands.Cog):
    def __init__(self, client):
        self.client = client
        print(f'Loaded', __name__)

    @commands.Cog.listener()
    async def on_ready(self):
        self.client.logging_channel = self.client.get_channel(
            self.client.settings["data"]["logging"]["channel"])
        self.client.logging_message = await self.client.logging_channel.fetch_message(
            self.client.settings["data"]["logging"]["message"])
        self.client.last_up = float(self.client.logging_message.content)
        hours, minutes, seconds = str(timedelta(
            seconds=round(time() - self.client.last_up))).split(":")
        if self.client.testing == False:
            await self.client.logging_channel.send(f"<@&922915340852289626> **The bot is back online, after being offline for ~`{hours} hour(s), {minutes} minute(s), {seconds} second(s)`.**\nCurrent bot version: {self.client.VERSION}\nCurrent pycord version: {discord.__version__}")
        while True:
            await asyncio.sleep(10)
            await self.client.logging_message.edit(content=str(time()))

    @commands.Cog.listener()
    async def on_command(self, ctx):
        if ctx.guild.id == 920662357372444672:
            return  # dont log if testing
        guild = ctx.guild.name
        author = f"{ctx.author.name}#{ctx.author.discriminator}"
        channel = ctx.channel.name
        command = ctx.message.content.replace(self.client.prefix, "")
        log = f"**{guild}:** *{author}* invoked `{command}` in `#{channel}`"
        await self.client.logging_channel.send(log)


def setup(client):
    client.add_cog(Logging(client))
