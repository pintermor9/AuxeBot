import asyncio
import discord
from io import StringIO
from discord.ext import commands


class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print(f"Loaded", __name__)

    @commands.command(name="view")
    async def _view(self, ctx):
        buttons = []
        for emoji in {
            "⏮️": "first",
            "⏪": "previous",
            "⏹": "stop",
            "⏩": "next",
            "⏭️": "last",
        }.keys():
            buttons.append(discord.ui.Button(emoji=emoji))

    @commands.command()
    async def readtxt(self, ctx, message_id, channel: discord.TextChannel = None):
        if channel is None:
            channel = ctx.channel
        message = await channel.fetch_message(message_id)
        bytes = await message.attachments[0].read()
        string = bytes.decode()
        while string != "":
            await ctx.send(string[:2000])
            string = string[2000:]

    @commands.command(
        name="run",
    )
    async def _run(self, ctx, script):
        _script = SCRIPTS[script]
        for full_command in _script:
            command_name = full_command.split(" ")[0]
            command = self.bot.get_command(command_name)
            await ctx.invoke(command, full_command.split(" ")[1:])

    @commands.command(name="run2")
    async def _run2(self, ctx, script_name):
        script = SCRIPTS[script_name]
        for full_command in script:
            command_name = full_command[0]
            command = self.bot.get_command(command_name)
            try:
                args = full_command[1]
            except IndexError:
                args = []
            await ctx.invoke(command, *args)
            await asyncio.sleep(1)


SCRIPTS = {"test": [["view"], ["help"], ["reverse", ["test"]]]}


async def setup(bot):
    await bot.add_cog(Test(bot))
