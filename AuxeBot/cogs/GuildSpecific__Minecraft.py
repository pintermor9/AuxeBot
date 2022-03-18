import discord
from discord.ext import commands, tasks

SERVERS = {
    "pintermor9_SERVER_0.aternos.me:12599": {
        "bedrock": False},
    "pintermor9_SERVER_2.aternos.me:64603": {
        "bedrock": True}}

API_URL = "https://api.mcsrvstat.us/{0}2/{1}"


class GuildSpecific__Minecraft(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print('Loaded', __name__)

    @commands.Cog.listener()
    async def on_ready(self):
        online = []
        for server in SERVERS.items():
            bedrock = "bedrock/" if server[1]["bedrock"] else ""
            response = await self.bot.api.get(API_URL.format(bedrock, server[0]), use_base=False)
            server = await response.json()
            print(server)
            if server["online"]:
                online.append(server)
        print(online)
        # self.check_servers.start()

    @tasks.loop(minutes=5)
    async def check_servers(self):
        online = []
        for server in SERVERS.items():
            bedrock = "bedrock/" if server[1]["bedrock"] else ""
            response = await self.bot.api.get(API_URL.format(bedrock, server[0]), use_base=False)
            server = await response.json()
            print(server)
            if server["online"]:
                online.append(server)
        print(online)


def setup(bot):
    return  # for now
    bot.add_cog(GuildSpecific__Minecraft(bot))
