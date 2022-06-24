import asyncio
import discord
from discord.ext import commands
import orjson


class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print(f"Loaded", __name__)

    @commands.command(name="view")
    async def _view(self, ctx):
        view = discord.ui.View()
        for emoji in {
            "⏮️": "first",
            "⏪": "previous",
            "⏹": "stop",
            "⏩": "next",
            "⏭️": "last",
        }.keys():
            view.add_item(discord.ui.Button(emoji=emoji))
        await ctx.send(
            "This is a test message",
            view=view)

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

    @commands.command(name="run")
    async def _run(self, ctx, script_name):
        script = SCRIPTS[script_name]
        for full_command in script:
            command = self.bot.get_command(full_command[0])
            kwargs = {} if len(full_command) == 1 else full_command[1]
            await command(ctx, **kwargs)


SCRIPTS = orjson.loads("""
{
    "test": [
        ["view"],
        ["reverse", {"text": "test"}]
    ]
}
""".strip())


async def setup(bot):
    await bot.add_cog(Test(bot))
