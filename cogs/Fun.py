import discord
from discord.ext import commands
import random
import requests


class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client
        print('Loaded', __name__)

    @commands.command(name='8ball', aliases=['eightball'], description="Gives you a random answer to your question.")
    async def _8ball(self, ctx, *, question):
        """Gives you a random answer to your question.
        Possible answers: *It is certain.*, *It is decidedly so.*, *Without a doubt.*, *Yes - definitely.*, *You may rely on it.*, *As I see it, yes.*, *Most likely.*, *Outlook good.*, *Yes.*, *Signs point to yes.*, *Reply hazy, try again.*, *Ask again later.*, *Better not tell you now.*, *Cannot predict now.*, *Concentrate and ask again.*, *Don't count on it.*, *My reply is no.*, *My sources say no.*, *Outlook not so good.*, *Very doubtful.*"""

        responses = ("It is certain.", "It is decidedly so.", "Without a doubt.", "Yes - definitely.", "You may rely on it.", "As I see it, yes.", "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.", "Reply hazy, try again.",
                     "Ask again later.", "Better not tell you now.", "Cannot predict now.", "Concentrate and ask again.", "Don't count on it.", "My reply is no.", "My sources say no.", "Outlook not so good.", "Very doubtful.")

        embed = discord.Embed(title=f'Answer: {random.choice(responses)}')
        embed.set_author(name=f'Your question: {question}')

        await ctx.send(embed=embed)

    @commands.command(aliases=['noice', 'nájsz', 'nojsz', 'nolysz'], description="Sends a nice gif.")
    async def nice(self, ctx):
        await ctx.send('https://www.icegif.com/wp-content/uploads/noice-icegif-3.gif')

    @commands.command(description="Sends a creepy gif.")
    async def creeper(self, ctx):
        await ctx.send('https://thumbs.gfycat.com/EntireReflectingKakarikis-size_restricted.gif')

    @commands.command(description="Chooses something from the given parameters.")
    async def choose(self, ctx, option_1, option_2, *more):
        chooselist = [option_1, option_2, *more]
        await ctx.send(random.choice(chooselist))

    @commands.command(aliases=['itsthisforthat', 'this/that', 'thisthat'], description="itsthisforthat.com")
    async def thisforthat(self, ctx):
        r = requests.get('http://itsthisforthat.com/api.php?json').json()
        thisforthat = r['this'], ' for ', r['that'], '!'
        await ctx.send(''.join(thisforthat))

    @commands.command(description="Echos/repeats the input text.")
    async def echo(self, ctx, *, text):
        await ctx.send(text)

    @commands.command(hidden=True)
    async def repeat(self, ctx, *, text):
        await ctx.message.delete()
        await ctx.send(text)

    @commands.command(description="Reverses the input text.")
    async def reverse(self, ctx, *, text):
        await ctx.send(text[-1::-1])


def setup(client):
    client.add_cog(Fun(client))
