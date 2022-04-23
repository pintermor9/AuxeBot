import logging
import discord
from discord.ext import commands
from discord.ext.commands.errors import *

logger = logging.getLogger(__name__)


class Error(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        logger.info("Loaded " + __name__)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        IGNORE = (CommandNotFound,)
        if isinstance(error, IGNORE):
            return

        DEAFULT = (
            BadArgument,
            BadUnionArgument,
            ArgumentParsingError,
            CheckFailure,
            DisabledCommand,
            CommandInvokeError,
            CommandOnCooldown,
            MaxConcurrencyReached,
        )

        embed = discord.Embed(
            title="Error:exclamation:", description="", color=0xFF0000
        )

        if isinstance(error, DEAFULT):
            embed.description = str(error)

        if isinstance(error, MissingRequiredArgument):
            embed.description = f"A required argument is missing: {error.param}"

        if isinstance(error, UserInputError):
            parent = ctx.command.parent.name + " " if ctx.command.parent else ""
            embed.add_field(
                name="Usage",
                value=f"`{parent + ctx.command.name} {ctx.command.signature.replace('=', ' = ')}".strip()
                + "`",
                inline=False,
            )

        await ctx.send(embed=embed)
        print(error)


def setup(bot):
    bot.add_cog(Error(bot))
