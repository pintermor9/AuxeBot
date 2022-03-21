import discord
from datetime import datetime
from discord.ext import commands, tasks

"""
Info
{
  "title": "Információ a szerverről",
  "description": "Ezt a szervert azért csináltam, hogy egyszerű legyen együtt Minecraftozni. (+ unatkoztam) ",
  "author": {
    "name": "Minecraft"
  },
  "color": 53380,
  "footer": {
    "text": "Köszönöm hogy végig olvastad! "
  },
  "fields": [
    {
      "name": "Reakció rangok",
      "value": "Itt tudjátok kiválasztani, hogy a Java, a Bedrock vagy mindkettő kiadással játszotok. Csak azokhoz a csatornákhoz kaptok hozzáférést, ami olyan szerverhez tartozik, amin tudtok játszani, az értesítések minimalizálása érdekében. \n#reakció-rangok",
      "inline": False 
    },
    {
      "name": "IP címek",
      "value": "A választott rangotok szerint hozzáférést kaptok az szerverek IP címeihez. Ebben a csatornában találjátok meg a felhasználónevet és jelszót ahhoz az [aternos](https://aternos.org) fiókhoz, amivel elindíthatjátok a szervereket. ",
      "inline": False 
    },
    {
      "name": "Szerver státusz",
      "value": "Itt látható, hogy jelenleg mely szerverek vannak online. \n#szerver-statusz",
      "inline": False
    }
  ]
}

Java Edition IP címek
{
    "title": "Java Edition IP címek",
    "fields": [
        {
            "name": "SERVER_0 - CROSSPLAY SURVIVAL",
            "value": "pintermor9_SERVER_0.aternos.me:12599"
        }, {
            "name": "SERVER_0 - SNAPSHOT TESTING", 
            "value": "pintermor9_SERVER_1.aternos.me:30946"
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
        },
        {
            "name": "Nem tudsz csatlakozni?",
            "value": "[Itt van segítség](https://wiki.geysermc.org/geyser/using-geyser-with-consoles/)! "
        }
    ]
}


Reakció rangok
{
    "title": "--              Reakció rangok              --",
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
        return int(server["players"]["max"]) > 1
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
            title="--              Online szerverek              --",
            timestamp=datetime.utcnow(), color=discord.Color.green())
        for server in self.online:
            embed.add_field(
                name=server["hostname"],
                value=f"{server['players']['online']}/{server['players']['max']}",
                inline=False)
        if len(self.online) == 0:
            embed.color = discord.Color.red()
            embed.description = "Jelenleg egy szerver sincs online. :("

        await self.message.edit(embeds=[embed])


def setup(bot):
    bot.add_cog(GuildSpecific__Minecraft(bot))
