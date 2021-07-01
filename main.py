print("Importing modules...")

import discord
from discord.ext import commands, tasks
import os
import yaml
from itertools import cycle

print("done.")
print("Getting client")

intents = discord.Intents.all()

def get_prefix(*args):
    return client.prefix

client = commands.Bot(command_prefix=get_prefix, help_command=None, intents=intents)

print("done.")
print("Reading settings...")

with open(r'./data/settings.yml') as file:
    settings = yaml.full_load(file)
    print(settings)

#General settings
client.prefix = settings['prefix']
TOKEN = settings['TOKEN']
client.owner_IDs = settings['owner_IDs']

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
    f'Prefix: {client.prefix}', f'Use \'{client.prefix}help\' for help!',
    'Owner: mor3000#8499',
    'Check out \'stats.uptimerobot.com/pLEoghzLzx\' for uptime stats!',
    'Yeah I know that I should get a profile picture.',
    f'Latest updates: {updates}'
])
# gets the apikey of https://Roboty-api.pintermor9.repl.co/
client.apikey = settings["apikey"]


print("done.")

if downAnnouncement:
    cycleActivities = False
    noCycleActivity = downAnnouncementStatus


def is_owner(ctx):
    return ctx.message.author.id in client.owner_IDs


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
    
    
@tasks.loop(seconds=10)
async def activityLoop():
    await client.change_presence(activity=discord.Game(next(loopActivities)))


for file in os.listdir('./cogs'):
    if file.endswith('.py'):
        client.load_extension(f'cogs.{file[:-3]}')

print("\n\nStarting client...\n")

client.run(TOKEN)
