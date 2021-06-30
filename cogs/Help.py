import discord
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, client):
        self.client = client
        print(f'Loaded', __name__)

    #COMMAND GROUP!
    # TAB!

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(description='These are the commands:', color=0x2F3136)
        embed.set_author(name="Help")
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.add_field(
            name="**Fun**",
            value="""

**8ball** <question> - *Gives you a random answer to your question!*
**nice** - *Sends a nice gif!*
**creeper** - *Sends a creepy gif!*
**choose** <1> <2> [3] [4] [5] [...] - *Chooses something from the given parameters!*
**reverse** <text> - *Reverses the inputted text!*

""",
            inline=False)

        embed.add_field(
            name="**Moderation**",
            value="""

**purge** <number> - *Clears a number of messages!*
**logout** - *Shuts down the bot!*
**ping** - *Pings the bot!*

""",
            inline=False)

#        embed.add_field(
#            name="**Levelling** | *You can earn levels by sending messages.*", 
#            value="""
#
#**rank** [person] - *Shows your XP, level, rank and a progress bar!*
#**leaderboard** [top] - *Shows the top 5 (by deafult) ranked people!*
#
#""",
#            inline=False)

        embed.set_footer(
            text=f"< > required, [ ] optional | Suggested by {ctx.author}.")

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Help(client))
