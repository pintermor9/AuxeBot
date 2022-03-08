import random
import discord
import aiohttp
from io import BytesIO
from typing import Union
from discord.ext import commands
from .Utils import Api

class Levelling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print(f'Loaded', __name__)

    def get_lvl(self, xp):
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
            old_xp = self.bot.data["levelling"][authorID]
        except KeyError:
            self.bot.data["levelling"].update({authorID: 0})
            old_xp = 0

        self.bot.data["levelling"][authorID] += random.randint(5, 12)
        xp = self.bot.data["levelling"][authorID]

        if self.get_lvl(old_xp)[1] < self.get_lvl(xp)[1]:
            await message.author.send(
                f"GG {message.author.mention}, you just advanced to level {self.get_lvl(xp)[1]}!"
            )

        self.bot.data["levelling"].update({authorID: xp})

    @commands.command(description="Shows the rank, level and xp of someone.")
    async def rank(self, ctx, user: Union[discord.Member, discord.User] = "you"):
        """Shows the rank, level and xp of someone. If you don't specify a user, it defaults to you."""
        async with ctx.typing():
            if user == "you":
                user = ctx.author

            try:
                xp = self.bot.data["levelling"][str(user.id)]
            except:
                self.bot.data["levelling"].update({str(user.id): 0})
                xp = self.bot.data["levelling"][str(user.id)]
            lvlxp, lvl = self.get_lvl(xp)

            rank = 1
            datalisted = sorted(self.bot.data["levelling"].items(),
                                key=lambda x: x[1], reverse=True)
            for x in datalisted:
                if x[0] == str(user.id):
                    break
                rank += 1
            try:
                if user.status == discord.Status.online:
                    status = "online"
                if user.status == discord.Status.offline:
                    status = "offline"
                if user.status == discord.Status.idle:
                    status = "idle"
                if user.status == discord.Status.dnd:
                    status = "dnd"
            except:
                status = "online"

            # async with aiohttp.ClientSession() as session:
            #     async with session.post("https://discord-bot-api.pintermor9.repl.co/rankcard/", data={
            #         "img": str(user.display_avatar if user.display_avatar != None else user.deafult_avatar),
            #         "currentXP": lvlxp,
            #         "requiredXP": int(200 * ((1 / 2) * lvl)),
            #         "status": status,
            #         "username": user.name,
            #         "discriminator": user.discriminator,
            #         "rank": rank,
            #         "level": lvl
            #     }) as response:
            #         if not str(response.status).startswith("2"):
            #             return await ctx.send(embed=discord.Embed(title="Sorry,", description="this is temporarily unavailable."))
            #         rankcard = await response.read()

            response = await Api.post(bot, "/rankcard", data={
                "img": str(user.display_avatar if user.display_avatar != None else user.deafult_avatar),
                "currentXP": lvlxp,
                "requiredXP": int(200 * ((1 / 2) * lvl)),
                "status": status,
                "username": user.name,
                "discriminator": user.discriminator,
                "rank": rank,
                "level": lvl})
            if not str(response.status).startswith("2"):
                return await ctx.send(embed=discord.Embed(title="Sorry,", description="this is temporarily unavailable."))
            rankcard = await response.read()

            await ctx.send(file=discord.File(BytesIO(rankcard), "rankcard.png"))

    @commands.command(aliases=["lead"], description="Shows the leaderboard.")
    async def leaderboard(self, ctx, top_x=5):
        """Shows the leaderboard. By default it will show the top 5 people, but you can specify a `top_x` argument."""
        async with ctx.typing():
            datalisted = sorted(self.bot.data["levelling"].items(),
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
                    user = self.bot.get_user(int(datalisted[rank][0]))
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


def setup(bot):
    bot.add_cog(Levelling(bot))
