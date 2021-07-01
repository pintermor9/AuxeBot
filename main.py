print("Importing modules...")

import discord
from discord.ext import commands, tasks
import os
import yaml
from itertools import cycle
from data.web import web

print("done.")
print("Reading settings...")

with open(r'./data/settings.yml') as file:
    settings = yaml.full_load(file)
    print(settings)

#General settings
prefix = settings['prefix']
TOKEN = settings['TOKEN']
owner_IDs = settings['owner_IDs']
webServer = settings['web']

#Downtime settings:
downAnnouncement = settings['downAnnouncement']
downDate = settings['downDate']
downAnnouncementStatus = settings['downAnnouncementStatus']

#Status and activity settings:
cycleActivities = settings['cycleActivities']
status = settings['status']
updates = settings['updates']
noCycleActivity = settings['noCycleActivity']
loopActivities = cycle([
    f'Prefix: {prefix}', f'Use \'{prefix}help\' for help!',
    'Owner: mor3000#8499',
    'Check out \'stats.uptimerobot.com/pLEoghzLzx\' for uptime stats!',
    'Yeah I know that I should get a profile picture.',
    f'Latest updates: {updates}'
])



print("done.")

intents = discord.Intents.all()

client = commands.Bot(command_prefix=prefix,
                      help_command=None,
                      intents=intents)

# gets the apikey of https://lvlsys-api.pintermor9.repl.co/
client.apikey = settings["apikey"]

if downAnnouncement:
    cycleActivities = False
    noCycleActivity = downAnnouncementStatus


def is_owner(ctx):
    return ctx.message.author.id in owner_IDs


@client.event
async def on_connect():
    print('Connected to discord.')
    print('Current discord.py version: {.__version__}'.format(discord))


@client.event
async def on_ready():
    print('Logged in as {0.user}!'.format(client))
    await client.change_presence(
        status=discord.Status.idle,
        activity=discord.Game("Initializing... Please wait."))

    if cycleActivities:
        activityLoop.start()
    else:
        await client.change_presence(activity=discord.Game(noCycleActivity))
    
    if webServer:
        web()

@tasks.loop(seconds=10)
async def activityLoop():
    await client.change_presence(activity=discord.Game(next(loopActivities)))


for file in os.listdir('./cogs'):
    if file.endswith('.py'):
        client.load_extension(f'cogs.{file[:-3]}')

print("\n\nStarting client...\n")

client.run(TOKEN)
