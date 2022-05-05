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
        b = discord.ui.Button(label="Test")

        async def cb(interaction):
            dir(interaction)

        b.callback = cb
        view = discord.ui.View(b)
        await ctx.send(view=view)

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


def setup(bot):
    bot.add_cog(Test(bot))
