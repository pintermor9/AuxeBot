import re
import discord
from io import StringIO
from discord.ext import commands


class Test(commands.Cog):
    def __init__(self, client):
        self.client = client
        print(f'Loaded', __name__)

    @commands.command()
    async def sendtxt(self, ctx, text):
        await ctx.send(file=discord.File(StringIO(str(text)), filename="message.json"))

    @commands.command()
    async def readtxt(self, ctx, message_id):
        message = await ctx.channel.fetch_message(message_id)
        bytes = await message.attachments[0].read()
        await ctx.send(bytes.decode())


def setup(client):
    client.add_cog(Test(client))
