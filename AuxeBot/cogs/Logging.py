import discord
import logging
from time import time
from datetime import timedelta
from discord.ext import commands

logger = logging.getLogger(__name__)


class Logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        logger.info("Loaded " + __name__)

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.logging_channel = self.bot.get_channel(
            self.bot.settings["data"]["logging"]["channel"]
        )

    @commands.Cog.listener()
    async def on_online(self):
        hours, minutes, seconds = str(
            timedelta(seconds=round(time() - float(self.bot.last_up)))
        ).split(":")

        if self.bot.testing == False:
            await self.bot.logging_channel.send(
                f"<@&922915340852289626> **The bot is back online, after being offline for ~`{hours} hour(s), {minutes} minute(s), {seconds} second(s)`.**\nCurrent bot version: {self.bot.VERSION}\nCurrent pycord version: {discord.__version__}"
            )

    @commands.Cog.listener()
    async def on_command(self, ctx):
        if ctx.guild.id == 920662357372444672:
            return  # dont log if testing
        guild = ctx.guild.name
        author = f"{ctx.author.name}#{ctx.author.discriminator}"
        channel = ctx.channel.name
        command = ctx.message.content[len(self.bot.prefix) :]
        log = f"**{guild}:** *{author}* invoked `{command}` in `#{channel}`"
        await self.bot.logging_channel.send(log)


async def setup(bot):
    await bot.add_cog(Logging(bot))
