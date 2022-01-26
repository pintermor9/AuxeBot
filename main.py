import os
import yaml
import discord
from Utils import Data
from itertools import cycle
from Help import HelpCommand
from discord.ext import commands, tasks

print('''         .d888888                              888888ba             dP   \n        d8'    88                              88    `8b            88   \n        88aaaaa88a dP    dP dP.  .dP .d8888b. a88aaaa8P' .d8888b. d8888P \n        88     88  88    88  `8bd8'  88ooood8  88   `8b. 88'  `88   88   \n        88     88  88.  .88  .d88b.  88.  ...  88    .88 88.  .88   88   \n        88     88  `88888P' dP'  `dP `88888P'  88888888P `88888P'   dP   \n                          Ascii art by patorjk.com                       ''')

LINE_CLEAR = "\x1b[2k"

print("Imported modules.", end=f"{LINE_CLEAR}\r")
print("Getting client...", end=f"{LINE_CLEAR}\r")

intents = discord.Intents.all()


def get_prefix(*_args):
    return client.prefix


client = commands.Bot(command_prefix=get_prefix,
                      help_command=HelpCommand(), intents=intents)


print("Done.", end=f"{LINE_CLEAR}\r")
print("Reading settings... ")

with open(r'./settings.yml') as file:
    settings = yaml.full_load(file)
    print(settings)

# General settings
TOKEN = os.environ["TOKEN"]
client.prefix = settings['prefix']
client.owner_IDs = settings['owner_IDs']
client.VERSION = settings['VERSION']
client.hidden_cogs = settings['hidden_cogs']

# Downtime settings:
downAnnouncement = settings['downAnnouncement']
downDate = settings['downDate']
downAnnouncementStatus = settings['downAnnouncementStatus']

# Status and activity settings:
cycleActivities = settings['cycleActivities']
status = settings['status']
updates = settings['updates']
noCycleActivity = settings['noCycleActivity']
loopActivities = cycle([
    f'Prefix: {client.prefix}', f'Use \'{client.prefix}help\' for help!',
    'Owner: mor3000#8499',
    'Check out \'stats.uptimerobot.com/pLEoghzLzx\' for uptime stats!',
    'Yeah I know that I should get a profile picture.',
    f'Latest updates: {updates}'
])

# get necessary info for logging and levelling
client.data = settings["data"]

client.WorkInProgressEmbed = discord.Embed(
    title="**Hello:exclamation:**", description="**The command that you invoked is not done yet.**\nSorry for the inconvenience.").set_footer(
        text="If you experience any bugs or mistakes, please use the \n`report` command, to report it to the owner")

client.settings = settings

try:
    client.testing = bool(os.environ["TESTING"])
except:
    client.testing = False

print("Done.", end=f"{LINE_CLEAR}\r")

if client.testing == True:
    cycleActivities = False
    noCycleActivity = "Currently testing..."
    client.load_extension("Test")


if downAnnouncement:
    cycleActivities = False
    noCycleActivity = downAnnouncementStatus


def is_owner(ctx):
    return ctx.message.author.id in client.owner_IDs


@client.event
async def on_connect():
    print('Connected to discord.')
    print(f'Current discord.py version: {discord.__version__}')
    print(f'Current bot version: {client.VERSION}')


@client.event
async def on_ready():
    print('Logged in as {.user}!'.format(client))
    await client.change_presence(
        status=discord.Status.idle,
        activity=discord.Game("Initializing... Please wait."))

    if cycleActivities:
        activityLoop.start()
    else:
        await client.change_presence(activity=discord.Game(noCycleActivity))

    message = client.settings["data"]["json-data"]
    client.data = await Data.load(client, message)

    dump_data.start()


@tasks.loop(seconds=15)
async def activityLoop():
    await client.change_presence(activity=discord.Game(next(loopActivities)))


@tasks.loop(seconds=30)
async def dump_data():
    message = client.settings["data"]["json-data"]
    if await Data.load(client, message) != client.data:
        await Data.dump(client, client.data, message)

client.load_extension("jishaku")
for file in os.listdir('./cogs'):
    if file.endswith('.py'):
        client.load_extension(f'cogs.{file[:-3]}')

print(" \n \nStarting client...\n ")

client.run(TOKEN)
