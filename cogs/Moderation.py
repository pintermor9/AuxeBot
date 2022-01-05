import discord
from discord.ext import commands


class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client
        print(f'Loaded', __name__)

    @commands.Cog.listener()
    async def on_ready(self):
        self.client.report_channel = self.client.get_channel(
            self.client.settings["data"]["report"]["channel"])

    @commands.command(description="Shows client ping.")
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.client.latency * 1000)}ms')

    @commands.command(aliases=['clear', 'cls'], description="Deletes a set amount of messages.")
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int):
        """Deletes a set amount of messages excluding the command."""
        await ctx.channel.purge(limit=(amount + 1))

    @commands.command(hidden=True)
    @commands.is_owner()
    async def logout(self, ctx):
        await ctx.send('Bye! :wave:')
        await self.client.change_presence(
            status=discord.Status.do_not_disturb,
            activity=discord.Game("Shutting down..."))
        await self.client.logout()
        exit(0)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def edit(self, ctx, channel: discord.TextChannel, message_id, content):
        message = await channel.fetch_message(message_id)
        if message.author != self.client.user:
            return await ctx.message.add_reaction(":x:")
        await message.edit(content=content)
        await ctx.message.delete()

    # TODO give XP boost to people who reported
    @commands.command(description="Sends a bug report to the owner.")
    async def report(self, ctx, *report):
        """Sends a bug report to the owner. The owner will review it and correct the mistake."""
        await ctx.message.add_reaction("✅")
        await self.client.report_channel.send(f"**author: {ctx.message.author.name}#{ctx.message.author.discriminator}**, guild: {ctx.guild.name}\n> {' '.join(report)}\nhttps://www.discord.com/channels/{ctx.guild.id}/{ctx.channel.id}/{ctx.message.id}")
        await ctx.send("**Thank you for reporting!** Please do not delete the command.")

    @commands.command(name='reload', hidden=True)
    @commands.is_owner()
    async def _reload(self, ctx, cog: str):
        self.client.unload_extension(cog)
        self.client.load_extension(cog)
        await ctx.message.add_reaction("✅")

    @commands.command(name='unload', hidden=True)
    @commands.is_owner()
    async def _unload(self, ctx, cog: str):
        self.client.unload_extension(cog)
        await ctx.message.add_reaction("✅")

    @commands.command(name='load', hidden=True)
    @commands.is_owner()
    async def _load(self, ctx, cog: str):
        self.client.load_extension(cog)
        await ctx.message.add_reaction("✅")


def setup(client):
    client.add_cog(Moderation(client))
