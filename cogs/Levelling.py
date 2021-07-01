import discord
from discord.ext import commands
import aiohttp
import random
import requests


class Levelling(commands.Cog):
    def __init__(self, client):
        self.client = client
        print(f'Loaded', __name__)

        self.client.levels = requests.get(f"https://roboty-api.pintermor9.repl.co/levels/?key={self.client.levelling_apikey}").json()

    def get_lvl(xp):
        lvl = 0
        while True:
            if xp < ((50 * (lvl**2)) + (50 * lvl)):
                xp -= ((50 * ((lvl - 1)**2)) + (50 * (lvl - 1)))
                return xp, lvl
            lvl += 1

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        authorID = str(message.author.id)
        try:
            old_xp = self.client.levels[authorID]
        except:
            old_xp = 0

        async with aiohttp.ClientSession() as session:
            xp = await session.get(f"https://roboty-api.pintermor9.repl.co/levels/add/{authorID}/{random.randint(10, 30)}/?key={self.client.levelling_apikey}")
            xp = await xp.json(); xp = xp[authorID]


        if Levelling.get_lvl(old_xp)[1] < Levelling.get_lvl(xp)[1]:
            channel = self.client.get_channel(768720147804192788)

            await channel.send(
                f"GG {message.author.mention}, you just advanced to level {Levelling.get_lvl(xp)[1]}!"
            )

        self.client.levels.update({authorID: xp})

    @commands.command()
    async def rank(self, ctx, user: discord.Member = None):
        msg = await ctx.send("Please wait...")

        if user == None:
            user = ctx.author

        try:
            xp = self.client.levels[str(user.id)]
        except:
            self.client.levels.update({str(user.id): 0})
            xp = self.client.levels[str(user.id)]

        lvlxp, lvl = Levelling.get_lvl(xp)

        boxnum = 25

        boxes = int((lvlxp / (200 * ((1 / 2) * lvl))) * boxnum)
        rank = 1

        datalisted = sorted(self.client.levels.items(), key=lambda x: x[1], reverse=True)
        

        for x in datalisted:
            if x[0] == str(user.id):
                break
            rank += 1

        if boxes < 10:
            embed = discord.Embed(title=f"{user}'s XP Stats", color=0xff0000)
        elif boxes < (boxnum - 5):
            embed = discord.Embed(title=f"{user}'s XP Stats", color=0xff8800)
        elif boxes >= (boxnum - 5):
            embed = discord.Embed(title=f"{user}'s XP Stats", color=0x00ff00)

        embed.add_field(name="Experience",
                        value=f"{lvlxp}/{int(200*((1/2)*lvl))}\n*Total: {xp}*",
                        inline=True)
        embed.add_field(name="Level", value=lvl, inline=True)
        embed.add_field(name="Rank", value=rank, inline=True)
        embed.add_field(name="Progress Bar",
                        value="".join((boxes * "█", (boxnum - boxes) * "░")),
                        inline=False)

        await msg.edit(embed=embed, content="")

    @commands.command(aliases=["lead"])
    async def leaderboard(self, ctx, top_x=5):
        msg = await ctx.send("Please wait...")

        datalisted = sorted(self.client.levels.items(),
                            key=lambda x: x[1], reverse=True)

        topIDs = tuple(map(lambda i: i[0], datalisted))

        if str(ctx.author.id) in topIDs:
            try:
                if topIDs.index(str(ctx.author.id)) == 0:
                    color = 0xff8800
                elif topIDs.index(str(ctx.author.id)) == 1:
                    color = 0xC0C0C0
                elif topIDs.index(str(ctx.author.id)) == 2:
                    color = 0xCC8833
                else:
                    raise Exception()
            except:
                color = 0x2F3136

        embed = discord.Embed(
            title="Leaderboard",
            description=f"Top {top_x} member(s) on the leaderboard\n",
            color=color)

        for rank in range(top_x):
            try:
                user = self.client.get_user(int(datalisted[rank][0]))
                xp = datalisted[rank][1]
            except:
                break

            lvlxp, lvl = Levelling.get_lvl(xp)
            whitespace = '\u2800' * (len(str(rank)) + 1)

            embed.add_field(
                name=f"**{rank + 1}.**\u2800{user}",
                value=f"**{whitespace} Level: {lvl},\u2800XP: {lvlxp}**",
                inline=False)

        await msg.edit(content=None, embed=embed)


def setup(client):
    client.add_cog(Levelling(client))
