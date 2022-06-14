import os
import ssl
import yaml
import orjson
import logging
import aiohttp
import certifi
from itertools import cycle

import discord
from discord.ext import commands, tasks

from Utils import Data, Api

logger = logging.getLogger(__name__)


def _get_prefix(bot, message):
    return commands.when_mentioned_or(bot.prefix)(bot, message)


class AuxeBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=_get_prefix,
            intents=discord.Intents.all()
        )

        with open(r"./settings.yml") as file:
            settings = yaml.full_load(file)
            logger.debug(settings)

        self.settings = settings

        self.prefix = settings["prefix"]
        self.VERSION = settings["VERSION"]
        self.hidden_cogs = settings["hidden_cogs"]

        # Status and activity settings:
        self.cycleActivities = settings["cycleActivities"]
        self.status = getattr(discord.Status, settings["status"])
        self.updates = settings["updates"]
        self.noCycleActivity = settings["noCycleActivity"]
        self.loopActivities = cycle(
            [
                f"Prefix: {self.prefix}",
                f"Use '{self.prefix}help' for help!",
                "Owner: GFIZ Auxea#8304",
                "Check out 'stats.uptimerobot.com/pLEoghzLzx' for uptime stats!",
                "Yeah, I know that I should get a profile picture.",
                f"Latest updates: {self.updates}",
            ]
        )

        self.data = settings["data"]

        self.WorkInProgressEmbed = discord.Embed(
            title="**Hello:exclamation:**",
            description="**The command that you invoked is not done yet.**\nSorry for the inconvenience.",
        ).set_footer(
            text="If you experience any bugs or mistakes, please use the \n`report` command, to report it to the owner"
        )

        self.settings = settings

        try:
            self.testing = bool(os.environ["TESTING"])
        except:
            self.testing = False

        if self.testing == True:
            self.cycleActivities = False
            self.noCycleActivity = "Currently testing..."

    async def on_ready(self):
        # Load extensions
        if self.testing:
            await self.load_extension("Test")

        await self.load_extension("jishaku")

        for file in os.listdir("./AuxeBot/cogs"):
            if file.endswith(".py"):
                await self.load_extension(f"cogs.{file[:-3]}")

        if getattr(super(), "on_ready", None):
            await super().on_ready()

        logger.info(f"Logged in as {self.user}!")
        message = self.settings["data"]["json-data"]
        self.data = await Data.load(self, message)

        if not self.testing:
            await self.change_presence(
                status=discord.Status.idle,
                activity=discord.Game("Initializing... Please wait."),
            )

            self.status = getattr(discord.Status, self.status)

            if self.cycleActivities:
                activityLoop.start(self)

            else:
                await self.change_presence(activity=discord.Game(self.noCycleActivity), status=self.status)

            dump_data.start(self)

            self.last_up = await self.api.get("/status/online")
            self.dispatch("online")

    async def on_connect(self):
        logger.info("Connected to discord.")
        logger.info(f"Current discord.py version: {discord.__version__}")
        logger.info(f"Current bot version: {self.VERSION}")

        session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(
            ssl=ssl.create_default_context(cafile=certifi.where())), json_serialize=orjson.dumps)
        self.api = Api(self, os.environ["API_SECRET"], session)

    async def close(self) -> None:
        print("AuxeBot is now closing...")

        await self.api.get("/status/offline")
        webhook = discord.Webhook.from_url(
            os.environ["offline_wh"], session=self.api.session
        )
        await webhook.send("<@&922915340852289626> **The bot went offline!**")
        await self.api.session.close()

        await super().close()

    def run(self):
        super().run(os.environ["TOKEN"], reconnect=True)


@tasks.loop(seconds=15)
async def activityLoop(bot):
    await bot.change_presence(activity=discord.Game(next(bot.loopActivities)))


@tasks.loop(seconds=30)
async def dump_data(bot):
    message = bot.settings["data"]["json-data"]
    if await Data.load(bot, message) != bot.data:
        await Data.dump(bot, bot.data, message)
