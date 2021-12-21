
from itertools import cycle
import json
import yaml
import os
from discord.ext import commands, tasks
import discord
print("Imported modules.")
print("Getting client...")

intents = discord.Intents.all()


def get_prefix(*args):
    return client.prefix


client = commands.Bot(command_prefix=get_prefix,
                      help_command=None, intents=intents)

print("done.")
print("Reading settings...")

with open(r'./settings.yml') as file:
    settings = yaml.full_load(file)
    print(settings)

# General settings
client.prefix = settings['prefix']
TOKEN = settings['TOKEN']
client.owner_IDs = settings['owner_IDs']

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

# gets the apikey of https://Roboty-api.pintermor9.repl.co/
client.levelling_apikey = settings["levelling_apikey"]
client.logging_apikey = settings["logging_apikey"]

# get necessary info for logging and levelling #! check later
client.data_guild_id = int(settings["data_guild_id"])

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

    client.data_guild = client.get_guild(client.data_guild_id)

    client.data_channels = client.data_guild.text_channels
    client.message_ids_channel = discord.utils.find(
        lambda channel: channel.name == 'message-ids', client.data_channels)
    client.message_ids = await client.message_ids_channel.fetch_message(client.message_ids_channel.last_message_id)
    client.message_ids = json.loads(client.message_ids.content)

    client.levelling_channel = discord.utils.find(
        lambda channel: channel.name == 'levelling-levels', client.data_channels)
    message_id = client.message_ids["levelling-levels"]
    client.levelling_message = await client.levelling_channel.fetch_message(message_id)
    client.levelling_levels = json.loads(client.levelling_message.content)

    if cycleActivities:
        activityLoop.start()
    else:
        await client.change_presence(activity=discord.Game(noCycleActivity))


def read_data(channel_id, message_id):
    message = client.data_guild.get_channel(
        channel_id).get_message(message_id).content
    print(message)


@tasks.loop(seconds=15)
async def activityLoop():
    await client.change_presence(activity=discord.Game(next(loopActivities)))


for file in os.listdir('./cogs'):
    if file.endswith('.py'):
        client.load_extension(f'cogs.{file[:-3]}')

print("\n\nStarting client...\n")

client.run(TOKEN)
