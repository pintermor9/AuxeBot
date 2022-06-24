import discord
import logging
from discord.ext import commands

logger = logging.getLogger(__name__)


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        logger.info("Loaded " + __name__)

    @commands.Cog.listener()
    async def on_ready_cogs(self):
        self.bot.report_channel = self.bot.get_channel(
            self.bot.settings["data"]["report"]["channel"]
        )

    @commands.command(description="Shows client ping.")
    async def ping(self, ctx):
        await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms")

    @commands.command(
        aliases=["clear", "cls"], description="Deletes a set amount of messages."
    )
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int):
        """Deletes a set amount of messages excluding the command."""
        await ctx.channel.purge(limit=(amount + 1))

    @commands.command(hidden=True)
    @commands.is_owner()
    async def shutdown(self, ctx):
        await ctx.send("Bye! :wave:")
        await self.bot.change_presence(
            status=discord.Status.do_not_disturb,
            activity=discord.Game("Shutting down..."),
        )
        await self.bot.close()
        exit(0)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def edit(self, ctx, channel: discord.TextChannel, message_id, content):
        message = await channel.fetch_message(message_id)
        if message.author != self.bot.user:
            return await ctx.message.add_reaction(":x:")
        await message.edit(content=content)
        await ctx.message.delete()

    # idea -- give XP boost to people who reported
    @commands.command(description="Sends a bug report to the owner.")
    async def report(self, ctx, *report):
        """Sends a bug report to the owner. The owner will review it and correct the mistake."""
        await ctx.message.add_reaction("✅")
        await self.bot.report_channel.send(
            f"**author: {ctx.message.author.name}#{ctx.message.author.discriminator}**, guild: {ctx.guild.name}\n> {' '.join(report)}\nhttps://www.discord.com/channels/{ctx.guild.id}/{ctx.channel.id}/{ctx.message.id}"
        )
        await ctx.send("**Thank you for reporting!** Please do not delete the command.")


async def setup(bot):
    await bot.add_cog(Moderation(bot))
