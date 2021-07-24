import discord
from discord.ext import commands


class Poll(commands.Cog):
    def __init__(self, client):
        self.client = client
        print(f'Loaded', __name__)


def setup(client):
    client.add_cog(Poll(client))
