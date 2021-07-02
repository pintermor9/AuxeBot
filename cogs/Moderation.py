import discord
from discord.ext import commands


class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client
        print(f'Loaded', __name__)

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.client.latency * 1000)}ms')

    @commands.command(aliases=['clear', 'cls'])
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int = None):
        if amount == None:
            await ctx.send('Please set an amount!')
        else:
            await ctx.channel.purge(limit=(amount + 1))

    @commands.command()
    @commands.is_owner()
    async def logout(self, ctx):
        await ctx.send('Bye! :wave:')
        await self.client.change_presence(
            status=discord.Status.do_not_disturb,
            activity=discord.Game("Shutting down..."))
        await self.client.logout()

    @commands.command()
    async def getctx(self, ctx):
        await ctx.message.delete()
        print(dict(ctx))
        await ctx.author.send(f'```python \n{dict(ctx)}\n```')
        await ctx.send('Context printed to console.', delete_after=5)

def setup(client):
    client.add_cog(Moderation(client))
