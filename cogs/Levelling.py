import json
import time
import discord
from discord.ext import commands
import aiohttp
import requests
import random


class Levelling(commands.Cog):
    def __init__(self, client):
        self.client = client
        print(f'Loaded', __name__)

    def get_lvl(self, xp):
        lvl = 0
        while True:
            if xp < ((50 * (lvl**2)) + (50 * lvl)):
                xp -= ((50 * ((lvl - 1)**2)) + (50 * (lvl - 1)))
                return xp, lvl
            lvl += 1

    @commands.Cog.listener()
    async def on_ready(self):
        self.client.levelling_channel = self.client.get_channel(
            self.client.data["levelling"]["channel"])
        self.client.levelling_message = await self.client.levelling_channel.fetch_message(
            self.client.data["levelling"]["message"])
        self.client.levelling_levels = json.loads(
            self.client.levelling_message.content)
        print(self.client.levelling_levels)

        # i delete users with no XP from dictionary (cleanup)
        self.client.levelling_levels = {
            member: xp for member, xp in self.client.levelling_levels.items() if xp != 0}
        await self.save_levels()

    async def save_levels(self):
        await self.client.levelling_message.edit(content=json.dumps(self.client.levelling_levels, indent=2))

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        authorID = str(message.author.id)
        try:
            old_xp = self.client.levelling_levels[authorID]
        except KeyError:
            self.client.levelling_levels.update({authorID: 0})
            old_xp = 0

        self.client.levelling_levels[authorID] += random.randint(10, 30)
        xp = self.client.levelling_levels[authorID]

        if self.get_lvl(old_xp)[1] < self.get_lvl(xp)[1]:
            await message.author.send(
                f"GG {message.author.mention}, you just advanced to level {self.get_lvl(xp)[1]}!"
            )

        self.client.levelling_levels.update({authorID: xp})
        await self.save_levels()

    @commands.command()
    async def rank(self, ctx, user: discord.User = "you"):
        async with ctx.typing():
            if user == "you":
                user = ctx.author

            try:
                xp = self.client.levelling_levels[str(user.id)]
            except:
                self.client.levelling_levels.update({str(user.id): 0})
                xp = self.client.levelling_levels[str(user.id)]

            lvlxp, lvl = self.get_lvl(xp)

            boxnum = 25

            boxes = int((lvlxp / (200 * ((1 / 2) * lvl))) * boxnum)
            rank = 1

            datalisted = sorted(self.client.levelling_levels.items(),
                                key=lambda x: x[1], reverse=True)

            for x in datalisted:
                if x[0] == str(user.id):
                    break
                rank += 1

            if boxes < 10:
                embed = discord.Embed(
                    title=f"{user}'s XP Stats", color=0xff0000)
            elif boxes < (boxnum - 5):
                embed = discord.Embed(
                    title=f"{user}'s XP Stats", color=0xff8800)
            elif boxes >= (boxnum - 5):
                embed = discord.Embed(
                    title=f"{user}'s XP Stats", color=0x00ff00)

            embed.add_field(name="Experience",
                            value=f"{lvlxp}/{int(200*((1/2)*lvl))}\n*Total: {xp}*",
                            inline=True)
            embed.add_field(name="Level", value=lvl, inline=True)
            embed.add_field(name="Rank", value=rank, inline=True)
            embed.add_field(name="Progress Bar",
                            value="".join(
                                (boxes * "█", (boxnum - boxes) * "░")),
                            inline=False)

            await ctx.send(embed=embed)

    @commands.command(aliases=["lead"])
    async def leaderboard(self, ctx, top_x=5):
        async with ctx.typing():
            datalisted = sorted(self.client.levelling_levels.items(),
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

                lvlxp, lvl = self.get_lvl(xp)
                whitespace = '\u2800' * (len(str(rank)) + 1)

                embed.add_field(
                    name=f"**`{rank + 1}`.** {user}",
                    value=f"** {whitespace} Level: {lvl},\u2800XP: {lvlxp}**",
                    inline=False)

            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Levelling(client))
