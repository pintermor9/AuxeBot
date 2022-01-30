import os
import yaml
import discord
import logging
from Utils import Data
from itertools import cycle
from discord.ext import commands, tasks

print('''         .d888888                              888888ba             dP   \n        d8'    88                              88    `8b            88   \n        88aaaaa88a dP    dP dP.  .dP .d8888b. a88aaaa8P' .d8888b. d8888P \n        88     88  88    88  `8bd8'  88ooood8  88   `8b. 88'  `88   88   \n        88     88  88.  .88  .d88b.  88.  ...  88    .88 88.  .88   88   \n        88     88  `88888P' dP'  `dP `88888P'  88888888P `88888P'   dP   \n                          Ascii art by patorjk.com                       ''')

LINE_CLEAR = "\x1b[2k"

print("Imported modules.", end=f"{LINE_CLEAR}\r")
print("Getting client...", end=f"{LINE_CLEAR}\r")


class Bot(commands.Bot):
    async def on_connect(self):
        print('Connected to discord.')
        print(f'Current discord.py version: {discord.__version__}')
        print(f'Current bot version: {self.VERSION}')
        await super().on_connect()

    async def on_ready(self):
        print('Logged in as {.user}!'.format(self))
        message = self.settings["data"]["json-data"]
        self.data = await Data.load(self, message)

        if not self.testing:
            await self.change_presence(
                status=discord.Status.idle,
                activity=discord.Game("Initializing... Please wait."))

            if status == "online":
                self.status = discord.Status.online
            if status == "idle":
                self.status = discord.Status.idle
            if status == "dnd":
                self.status = discord.Status.dnd
            if cycleActivities:
                activityLoop.start()
            else:
                await self.change_presence(activity=discord.Game(noCycleActivity), status=status)

            dump_data.start()

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


print("Done.", end=f"{LINE_CLEAR}\r")
print("Reading settings... ")

with open(r'./settings.yml') as file:
    settings = yaml.full_load(file)
    print(settings)

# General settings
TOKEN = os.environ["TOKEN"]
bot.prefix = settings['prefix']
bot.owner_IDs = settings['owner_IDs']
bot.VERSION = settings['VERSION']
bot.hidden_cogs = settings['hidden_cogs']


# Status and activity settings:
cycleActivities = settings['cycleActivities']
status = settings['status']
updates = settings['updates']
noCycleActivity = settings['noCycleActivity']
loopActivities = cycle([
    f'Prefix: {bot.prefix}', f'Use \'{bot.prefix}help\' for help!',
    'Owner: mor3000#8499',
    'Check out \'stats.uptimerobot.com/pLEoghzLzx\' for uptime stats!',
    'Yeah I know that I should get a profile picture.',
    f'Latest updates: {updates}'
])

# get necessary info for logging and levelling
bot.data = settings["data"]

bot.WorkInProgressEmbed = discord.Embed(
    title="**Hello:exclamation:**", description="**The command that you invoked is not done yet.**\nSorry for the inconvenience.").set_footer(
        text="If you experience any bugs or mistakes, please use the \n`report` command, to report it to the owner")

bot.settings = settings

try:
    bot.testing = bool(os.environ["TESTING"])
except:
    bot.testing = False

logging.basicConfig(
    level="INFO" if not bot.testing else settings["log_level"])

print("Done.", end=f"{LINE_CLEAR}\r")

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

bot.load_extension("jishaku")
for file in os.listdir('./cogs'):
    if file.endswith('.py'):
        bot.load_extension(f'cogs.{file[:-3]}')

print(" \n \nStarting client...\n ")

bot.run(TOKEN)
