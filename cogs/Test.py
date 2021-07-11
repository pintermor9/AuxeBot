import discord
from discord.ext import commands
import DiscordUtils
from asyncio import sleep

class Test(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def paginate(self, ctx):
        embed1 = discord.Embed(color=ctx.author.color).add_field(name="Example", value="Page 1")
        embed2 = discord.Embed(color=ctx.author.color).add_field(name="Example", value="Page 2")
        embed3 = discord.Embed(color=ctx.author.color).add_field(name="Example", value="Page 3")
        paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, remove_reactions=True)
        paginator.add_reaction('⏮️', "first")
        paginator.add_reaction('⏪', "back")
        paginator.add_reaction('🔐', "lock")
        paginator.add_reaction('⏩', "next")
        paginator.add_reaction('⏭️', "last")
        embeds = [embed1, embed2, embed3]
        await paginator.run(embeds)

    @commands.command()
    async def typing(self, ctx):
        async with ctx.typing():
            # do expensive stuff here
            await sleep(5)
            await ctx.send('done!')


def setup(client):
    client.add_cog(Test(client))
