import discord
import logging
from discord.ext import commands
from discord import app_commands

logger = logging.getLogger(__name__)


class Guild__VALORANT_HUN(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        logger.info('Loaded', __name__)

    @app_commands.command()
    async def create(self, interaction: discord.Interaction):
        await interaction.send_message('Create')


async def setup(bot):
    await bot.add_cog(Guild__VALORANT_HUN(bot))
