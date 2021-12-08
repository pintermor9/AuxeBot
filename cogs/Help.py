import discord
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, client):
        self.client = client
        print(f'Loaded', __name__)

    # COMMAND GROUP!
    # TAB!

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(
            description='These are the commands:', color=0x2F3136)
        embed.set_author(name="Help")
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.add_field(
            name="**Fun**",
            value="""

**8ball** <question> - *Gives you a random answer to your question!*
**nice** - *Sends a nice gif!*
**creeper** - *Sends a creepy gif!*
**choose** <1> <2> [3] [4] [5] [...] - *Chooses something from the given parameters!*
**echo** <text> - *Echos the inputted text!*
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

        embed.add_field(
            name="**Levelling** | *You can earn levels by sending messages.*",
            value="""

**rank** [person] - *Shows your XP, level, rank and a progress bar!*
**leaderboard** [top] - *Shows the top 5 (by deafult) ranked people!*

""",
            inline=False)

        embed.add_field(
            name="**Music**",
            value="""

**join** - *Joins your voice channel.*
**summon** [voice channel id] - *Summons the bot to a specified voice channel.*
**leave** - *Clears the queue and leaves the voice channel.*
**volume** <volume> - *Sets the volume of the player.* `WIP`
**now** - *Displays the currently playing song.*
**pause** - *Pauses the currently playing song.*
**resume** - *Pauses the paused song.*
**stop** - *Stops playing song and clears the queue.*
**skip** - *Skips the currently playing song.*
**queue** [page: 1] - *Shows the player's queue.*
**shuffle** - *Shuffles the queue.*
**remove** - *Removes a song from the queue at a given index.*
**loop** - *Loops the currently playing song.*
**play** [title/youtube url] - *If not in voice channel, invokes `join`. Plays or enqueues a song.*

""",
            inline=False)

        embed.set_footer(
            text=f"< > required, [ ] optional | Suggested by {ctx.author}.")

        await ctx.send(embed=embed)

    @commands.command()
    async def info(self, ctx):
        embed = discord.Embed(
            title="Info about the bot",
            description="Source code: https://bit.ly/roboty-source")
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Help(client))
