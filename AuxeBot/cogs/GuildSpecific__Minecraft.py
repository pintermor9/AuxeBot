import json
import discord
from discord.ext import commands, tasks
import orjson

SERVERS = {
    "pintermor9_SERVER_0.aternos.me:12599": {
        "bedrock": False},
    "pintermor9_SERVER_2.aternos.me:64603": {
        "bedrock": True},
    "mc.hypixel.net": {
        "bedrock": False}}

API_URL = "https://api.mcsrvstat.us/{0}2/{1}"


def is_online(server):
    try:
        return int(server["players"]["online"]) > 0
    except:
        return False


class GuildSpecific__Minecraft(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print('Loaded', __name__)

    @commands.Cog.listener()
    async def on_ready(self):
        self.check_servers.start()

    @tasks.loop(minutes=5)
    async def check_servers(self):
        online = []
        for server in SERVERS.items():
            try:
                bedrock = "bedrock/" if server[1]["bedrock"] else ""
                server = await self.bot.api.get(API_URL.format(bedrock, server[0]), use_base=False, return_as="json")
                if is_online(server):
                    online.append(server)
            except:
                continue
        print(online)
        print(len(online))


def setup(bot):
    return  # for now
    bot.add_cog(GuildSpecific__Minecraft(bot))
