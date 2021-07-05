import discord
from discord.ext import commands
import random
import requests


class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client
        print('Loaded', __name__)

    @commands.command()
    async def reverse(self, ctx, *, text):
        await ctx.send(text[-1::-1])

    @commands.command(name='8ball', aliases=['eightball'])
    async def _8ball(self, ctx, *, question=None):
        if question == None:
            await ctx.send('Please ask a question!')
        else:
            responses = [
                "It is certain.",
                "It is decidedly so.",
                "Without a doubt.",
                "Yes - definitely.",
                "You may rely on it.",
                "As I see it, yes.",
                "Most likely.",
                "Outlook good.",
                "Yes.",
                "Signs point to yes.",
                "Reply hazy, try again.",
                "Ask again later.",
                "Better not tell you now.",
                "Cannot predict now.",
                "Concentrate and ask again.",
                "Don't count on it.",
                "My reply is no.",
                "My sources say no.",
                "Outlook not so good.",
                "Very doubtful."
            ]

            embed = discord.Embed(title=f'Answer: {random.choice(responses)}')
            embed.set_author(name=f'Your question: {question}')

            await ctx.send(embed=embed)

    @commands.command(aliases=['noice', 'nájsz', 'nojsz', 'nolysz'])
    async def nice(self, ctx):
        await ctx.send('https://www.icegif.com/wp-content/uploads/noice-icegif-3.gif')

    @commands.command()
    async def creeper(self, ctx):
        await ctx.send('https://thumbs.gfycat.com/EntireReflectingKakarikis-size_restricted.gif')

    @commands.command()
    async def choose(self, ctx, _1, _2, *more):
        chooselist = [_1, _2]
        chooselist.extend(more)
        await ctx.send(random.choice(chooselist))

    @commands.command(aliases=['itsthisforthat', 'this/that', 'thisthat'])
    async def thisforthat(self, ctx):
        r = requests.get('http://itsthisforthat.com/api.php?json').json()
        thisforthat = r['this'], ' for ', r['that'], '!'
        await ctx.send(''.join(thisforthat))

    @commands.command()
    async def echo(self, ctx, *, text):
        await ctx.send(text)


def setup(client):
    client.add_cog(Fun(client))
