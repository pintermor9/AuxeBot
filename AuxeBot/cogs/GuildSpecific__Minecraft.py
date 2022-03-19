import json
import discord
from discord.ext import commands, tasks
import orjson

"""
Java Edition IP címek
    {
        "title": "Java Edition IP címek",
        "fields": [
            {
                "name": "SERVER_0 - CROSSPLAY SURVIVAL",
                "value": "pintermor9_SERVER_0.aternos.me:12599"
            }
        ],
        "footer": {
            "text": 'A kettőspont utáni számokat nem kötelező beírni. \nHa, TLaunchert vagy más tört verziót használsz, \nvagy "SRV" hibát dob fel a játék, írd oda!'
        }
    }

Bedrock Edition IP címek
    {
        "title": "Bedrock Edition IP címek",
        "fields": [
            {
                "name": "SERVER_0 - CROSSPLAY SURVIVAL",
                "value": "CÍM: pintermor9_SERVER_0.aternos.me\nPORT: 12599"
            }
        ]
    }


{
    "title": "--                                          Reakció rangok                                          --",
    "description": "Kérlek reagálj erre az üzentre, a játékod kiadásának megfelelő emojival:",
    "fields": [
        {
            "name": "Java Edition",
            "value": ":javaEdition:",
            "inline": True
        }, {
            "name": "Bedrock Edition",
            "value": ":bedrockEdition:",
            "inline": True
        }
    ]
}
"""

SERVERS = {
    "pintermor9_SERVER_0.aternos.me:12599": {
        "bedrock": False},
    "pintermor9_SERVER_2.aternos.me:64603": {
        "bedrock": True}}

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
        self.channel = self.bot.get_channel(
            self.bot.settings["data"]["minecraft"]["channel"])
        self.message = await self.channel.fetch_message(
            self.bot.settings["data"]["minecraft"]["message"])

        self.check_servers.start()

    @tasks.loop(minutes=5)
    async def check_servers(self):
        self.online = []
        for server in SERVERS.items():
            try:
                bedrock = "bedrock/" if server[1]["bedrock"] else ""
                server = await self.bot.api.get(API_URL.format(bedrock, server[0]), use_base=False, return_as="json")
                if is_online(server):
                    self.online.append(server)
            except:
                continue

        await self.edit_server_list()

    async def edit_server_list(self):
        embed = discord.Embed(
            title="--              Online szerverek              --")
        for server in self.online:
            embed.color = discord.Color.green()
            embed.add_field(
                name=server["hostname"],
                value=f"{server['players']['online']}/{server['players']['max']}",
                inline=False)
        if len(self.online) == 0:
            embed.color = discord.Color.red()
            embed.description = "Jelenleg egy szerver sincs online. :("

        await self.message.edit(embeds=[embed])


def setup(bot):
    # return  # for now
    bot.add_cog(GuildSpecific__Minecraft(bot))
