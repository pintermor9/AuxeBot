import re
import discord
from discord.ext import commands


class Test(commands.Cog):
    def __init__(self, client):
        self.client = client
        print(f'Loaded', __name__)

    @commands.command()  # todo make these failsafe (if theres & or $ in the text ingnore them.)
    async def readmessage(self, ctx, message_id):
        message = await ctx.channel.fetch_message(message_id)
        texts = []
        while re.search(r"[$][\d]+$", message.content):
            next_message = re.search(
                r"[$][\d]+$", message.content).group(0).replace("$", "")
            texts.append(message.content.replace(
                "$" + next_message, "").replace("&", ""))
            message = await ctx.channel.fetch_message(int(next_message))
        texts.append(message.content.replace("$last", "").replace("&", ""))
        await ctx.send("".join(reversed(texts)))

    @commands.command()
    async def parsemessage(self, ctx, text):
        chunk = text[:20]
        last_message = await ctx.send(f"&{chunk}$last")
        text = text.replace(chunk, "")
        while len(text) > 0:
            chunk = text[:20]
            last_message = await ctx.send(f"&{chunk}${last_message.id}")
            text = text.replace(chunk, "")

    @commands.command()
    async def sendtxt(self, ctx, text):
        await ctx.send(file=discord.File(SttingIo(str(text))))


def setup(client):
    client.add_cog(Test(client))
