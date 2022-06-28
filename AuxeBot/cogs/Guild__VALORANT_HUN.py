import asyncio
import discord
import logging
from discord.ext import commands
from discord import app_commands

from Utils import get_category

logger = logging.getLogger(__name__)


class Guild__VALORANT_HUN(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        logger.info('Loaded ' + __name__)

    @app_commands.command(name="create", description="Lobby létrehozása")
    @app_commands.describe(message="Az üzenet ami ki lessz írva a lobbydhoz.")
    async def create(self, interaction: discord.Interaction, message: str):
        await interaction.response.defer(thinking=False)
        user = interaction.user
        if not user.voice or not user.voice.channel.id == 991046332280107028:
            return await interaction.response.send_message("Lépj be a 'Váró' hangcsatornába mielőtt ezt a parancsot használod!", ephemeral=True)

        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False),
            user: discord.PermissionOverwrite(view_channel=True, speak=True, connect=True),
        }
        voice_channel = await interaction.guild.create_voice_channel(
            name="Lobby #1234",
            category=get_category(interaction.guild, 991067190662950932),
            overwrites=overwrites
        )
        await user.move_to(voice_channel)
        await interaction.followup.send(f"{user.mention}\n{message}\nRangja: {'TODO'}")

    @app_commands.command(name="join", description="Csatlakozás egy lobbyhoz")
    @app_commands.describe(member="Akinek a lobbyjához szeretnél csatlakozni.")
    async def join(self, interaction: discord.Interaction, member: discord.Member):
        await interaction.response.defer(thinking=False)


async def setup(bot):
    return
    await bot.add_cog(Guild__VALORANT_HUN(bot))
