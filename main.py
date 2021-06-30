import discord
from discord.ext import commands, tasks
import os
import yaml
from itertools import cycle
from keep_alive import keep_alive

with open(r'./data/settings.yml') as file:
	settings = yaml.full_load(file)
	print(settings)

#General settings
prefix = settings['prefix']
if settings['TOKEN'] == "os.getenv('TOKEN')" or settings[
        'TOKEN'] == 'os.getenv("TOKEN")':
	TOKEN = os.getenv('TOKEN')
else:
	TOKEN = settings['TOKEN']
webServer = settings['webServer']
owner_IDs = settings['owner_IDs']

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

intents = discord.Intents.all()

client = commands.Bot(command_prefix=prefix,
                      help_command=None,
                      intents=intents)

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

	if webServer:
		keep_alive()

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

client.run(TOKEN)
