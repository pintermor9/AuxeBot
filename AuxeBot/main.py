import os
import ssl
import yaml
import Utils
import orjson
import discord
import aiohttp
import logging
import certifi
import logging
from Utils import Data
from itertools import cycle
from discord.ext import commands, tasks

logger = logging.getLogger(__name__)


print(
    """         .d888888                              888888ba             dP   \n        d8'    88                              88    `8b            88   \n        88aaaaa88a dP    dP dP.  .dP .d8888b. a88aaaa8P' .d8888b. d8888P \n        88     88  88    88  `8bd8'  88ooood8  88   `8b. 88'  `88   88   \n        88     88  88.  .88  .d88b.  88.  ...  88    .88 88.  .88   88   \n        88     88  `88888P' dP'  `dP `88888P'  88888888P `88888P'   dP   \n                          Ascii art by patorjk.com                       """
)


logger.info("Imported modules.")
logger.info("Getting client...")


class Bot(commands.Bot):
    async def on_connect(self):
        logger.info("Connected to discord.")
        logger.info(f"Current discord.py version: {discord.__version__}")
        logger.info(f"Current bot version: {self.VERSION}")

        self.utils = Utils
        session = aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(
                ssl=ssl.create_default_context(cafile=certifi.where())
            ),
            json_serialize=orjson.dumps,
        )
        self.api = Utils.Api(self, os.environ["API_SECRET"], session)

        await super().on_connect()

    async def on_ready(self):
        logger.info("Logged in as {.user}!".format(self))
        message = self.settings["data"]["json-data"]
        self.data = await Data.load(self, message)

        if not self.testing:
            await self.change_presence(
                status=discord.Status.idle,
                activity=discord.Game("Initializing... Please wait."),
            )

            self.status = discord.Status.__dict__[status]

            if cycleActivities:
                activityLoop.start()

            else:
                await self.change_presence(
                    activity=discord.Game(noCycleActivity), status=status
                )

            dump_data.start()
            bot_status.start()

    async def on_message(self, message):
        if not self.testing and not message.channel.id == 937293407796207627:
            return await super().on_message(message)
        elif self.testing and message.channel.id == 937293407796207627:
            return await super().on_message(message)
        else:
            return


intents = discord.Intents.all()


def get_prefix(*_args):
    return bot.prefix


bot = Bot(command_prefix=get_prefix, intents=intents)


logger.info("Done.")
logger.info("Reading settings... ")

with open(r"./settings.yml") as file:
    settings = yaml.full_load(file)
    logger.debug(settings)

# General settings
TOKEN = os.environ["TOKEN"]
bot.prefix = settings["prefix"]
bot.owner_IDs = settings["owner_IDs"]
bot.VERSION = settings["VERSION"]
bot.hidden_cogs = settings["hidden_cogs"]


# Status and activity settings:
cycleActivities = settings["cycleActivities"]
status = settings["status"]
updates = settings["updates"]
noCycleActivity = settings["noCycleActivity"]
loopActivities = cycle(
    [
        f"Prefix: {bot.prefix}",
        f"Use '{bot.prefix}help' for help!",
        "Owner: GFIZ Auxea#8304",
        "Check out 'stats.uptimerobot.com/pLEoghzLzx' for uptime stats!",
        "Yeah, I know that I should get a profile picture.",
        f"Latest updates: {updates}",
    ]
)

bot.data = settings["data"]

bot.WorkInProgressEmbed = discord.Embed(
    title="**Hello:exclamation:**",
    description="**The command that you invoked is not done yet.**\nSorry for the inconvenience.",
).set_footer(
    text="If you experience any bugs or mistakes, please use the \n`report` command, to report it to the owner"
)

bot.settings = settings


try:
    bot.testing = bool(os.environ["TESTING"])
except:
    bot.testing = False

try:
    assert bot.testing
    level = __import__("inputimeout").inputimeout(
        "Do you want to set logging level to DEBUG (y/n): ", timeout=5
    )
    assert level.lower() == "y"
    level = logging.DEBUG
except:
    level = logging.INFO
finally:
    logging.basicConfig(level=level)


logger.info("Done.")

if bot.testing == True:
    cycleActivities = False
    noCycleActivity = "Currently testing..."
    bot.load_extension("Test")


def is_owner(ctx):
    return ctx.message.author.id in bot.owner_IDs


@tasks.loop(seconds=15)
async def activityLoop():
    await bot.change_presence(activity=discord.Game(next(loopActivities)))


@tasks.loop(seconds=30)
async def dump_data():
    message = bot.settings["data"]["json-data"]
    if await Data.load(bot, message) != bot.data:
        await Data.dump(bot, bot.data, message)


@tasks.loop(minutes=1)
async def bot_status():
    await bot.api.get("/status/ping")


@bot_status.before_loop
async def status_online():
    bot.last_up = await bot.api.get("/status/online")
    bot.dispatch("online")


@bot_status.after_loop
async def status_offline():
    await bot.api.get("/status/offline")

    webhook = discord.Webhook.from_url(
        os.environ["offline_wh"], session=bot.api.session
    )
    await webhook.send("<@&922915340852289626> **The bot went offline!**")

    await bot.api.session.close()


bot.load_extension("jishaku")
for file in os.listdir("./AuxeBot/cogs"):
    if file.endswith(".py"):
        bot.load_extension(f"cogs.{file[:-3]}")

logger.info(" \n \nStarting client...\n ")

if __name__ == "__main__":
    bot.run(TOKEN)

"""
# test run always restart
import os
while True: 
    try:
        print('\n'*100); os.system("py AuxeBot/main.py");
    except KeyboardInterrupt:
        input()
    except:
        pass
"""
