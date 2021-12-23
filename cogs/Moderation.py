import asyncio
import discord
from discord import message
from discord.ext import commands


class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client
        print(f'Loaded', __name__)

    @commands.Cog.listener()
    async def on_ready(self):
        self.client.report_channel = self.client.get_channel(
            self.client.data["report"]["channel"])

    @commands.command(description="")
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.client.latency * 1000)}ms')

    @commands.command(aliases=['clear', 'cls'], description="")
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int = None):
        if amount == None:
            await ctx.send('Please set an amount!')
        else:
            await ctx.channel.purge(limit=(amount + 1))

    @commands.command(hidden=True)
    @commands.is_owner()
    async def logout(self, ctx):
        await ctx.send('Bye! :wave:')
        await self.client.change_presence(
            status=discord.Status.do_not_disturb,
            activity=discord.Game("Shutting down..."))
        await self.client.logout()

    @commands.command(hidden=True)
    @commands.is_owner()
    async def edit(self, ctx, channel: discord.TextChannel, message_id, content):
        message = await channel.fetch_message(message_id)
        if message.author != self.client.user:
            return await ctx.message.add_reaction(":x:")
        await message.edit(content=content)
        await ctx.message.delete()

    @commands.command()
    async def report(self, ctx, *report):
        await ctx.message.add_reaction("✅")
        await self.client.report_channel.send(f"**author: {ctx.message.author.name}#{ctx.message.author.discriminator}**, guild: {ctx.guild.name}\n> {' '.join(report)}\nhttps://www.discord.com/channels/{ctx.guild.id}/{ctx.channel.id}/{ctx.message.id}")
        await ctx.send("**Thank you for reporting!** Please do not delete the command.")


def setup(client):
    client.add_cog(Moderation(client))
