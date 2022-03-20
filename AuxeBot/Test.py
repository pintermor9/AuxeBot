import discord
from io import StringIO
from discord.ext import commands


class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print(f'Loaded', __name__)

    @commands.command()
    async def sendtxt(self, ctx, text):
        await ctx.send(file=discord.File(StringIO(str(text)), filename="message.json"))

    @commands.command()
    async def readtxt(self, ctx, message_id):
        message = await ctx.channel.fetch_message(message_id)
        bytes = await message.attachments[0].read()
        await ctx.send(bytes.decode())

    @commands.command()
    async def fixshopthreads(self, ctx):
        for thread in await ctx.channel.archived_threads().flatten():
            if not thread.name.endswith(" - before timestamp"):
                continue
            await thread.unarchive()
            await thread.edit(name=thread.name.replace(" - before timestamp", ""))
            await thread.archive()

    @commands.command()
    async def test(self, ctx):
        self.bot.dispatch("test")

    @commands.Cog.listener("on_test")
    async def on_test(self):
        print("IDK")


def setup(bot):
    bot.add_cog(Test(bot))
