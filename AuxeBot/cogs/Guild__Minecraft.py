import logging
import discord
from datetime import datetime
from discord.ext import commands, tasks

logger = logging.getLogger(__name__)


class Embeds:
    locations = {
        "Info": [954267475388817438, 954771976944250971],
        "JavaIPs": [954267709326098432, 954766315992809515],
        "BedrockIPs": [954267747238424616, 954765517971918878],
        "ReactionRoles": [954267562470961193, 954712865191903232],
        "Access": [954267709326098432, 954766315992809515],
        "BAccess": [954267747238424616, 954765517971918878],
    }

    Info = discord.Embed.from_dict(
        {
            "title": "Információ a szerverről",
            "description": "Ezt a szervert azért csináltam, hogy egyszerű legyen együtt Minecraftozni. (+ unatkoztam) ",
            "author": {"name": "Minecraft"},
            "color": 53380,
            "footer": {"text": "Köszönöm hogy végig olvastad! "},
            "fields": [
                {
                    "name": "Reakció rangok",
                    "value": "Itt tudjátok kiválasztani, hogy a Java, a Bedrock vagy mindkettő kiadással játszotok. Csak azokhoz a csatornákhoz kaptok hozzáférést, ami olyan szerverhez tartozik, amin tudtok játszani, az értesítések minimalizálása érdekében. \n#reakció-rangok",
                    "inline": False,
                },
                {
                    "name": "IP címek",
                    "value": "A választott rangotok szerint hozzáférést kaptok az szerverek IP címeihez. Ebben a csatornában találjátok meg a felhasználónevet és jelszót ahhoz az [aternos](https://aternos.org) fiókhoz, amivel elindíthatjátok a szervereket. ",
                    "inline": False,
                },
                {
                    "name": "Szerver státusz",
                    "value": "Itt látható, hogy jelenleg mely szerverek vannak online. \n#szerver-statusz",
                    "inline": False,
                },
            ],
        }
    )

    JavaIPs = discord.Embed.from_dict(
        {
            "title": "Java Edition IP címek",
            "fields": [
                {
                    "name": "SERVER_0 - CROSSPLAY SURVIVAL",
                    "value": "pintermor9_SERVER_0.aternos.me:12599",
                },
                {
                    "name": "SERVER_0 - SNAPSHOT TESTING",
                    "value": "pintermor9_SERVER_1.aternos.me:30946",
                },
            ],
            "footer": {
                "text": 'A kettőspont utáni számokat nem kötelező beírni. \nHa, TLaunchert vagy más tört verziót használsz, \nvagy "SRV" hibát dob fel a játék, írd oda!'
            },
        }
    )

    BedrockIPs = discord.Embed.from_dict(
        {
            "title": "Bedrock Edition IP címek",
            "fields": [
                {
                    "name": "SERVER_0 - CROSSPLAY SURVIVAL",
                    "value": "CÍM: pintermor9_SERVER_0.aternos.me\nPORT: 12599",
                },
                {
                    "name": "Nem tudsz csatlakozni?",
                    "value": "[Itt van segítség](https://wiki.geysermc.org/geyser/using-geyser-with-consoles/)! ",
                },
            ],
        }
    )

    ReactionRoles = discord.Embed.from_dict(
        {
            "title": "--              Reakció rangok              --",
            "description": "Kérlek reagálj erre az üzentre, a játékod kiadásának megfelelő emojival:",
            "fields": [
                {
                    "name": "Java Edition",
                    "value": "<:javaEdition:954709973408030740>",
                    "inline": True,
                },
                {
                    "name": "Bedrock Edition",
                    "value": "<:bedrockEdition:954710184045998100>",
                    "inline": True,
                },
            ],
        }
    )

    Access = discord.Embed.from_dict(
        {
            "title": "Aternos indítási hozzáférés",
            "description": "Itt vannak a bejelentkezési adatok ahhoz az [aternos](https://aternos.org/servers) fiókhoz, amivel el tudjátok indítani a szervereket.\n**Felhasználónév:** pintermor9_Access\n**Jelszó:** access.aternos\n**Kérlek ne változtassad meg a jelszót!**",
        }
    )

    BAccess = discord.Embed.from_dict(
        {
            "title": "Aternos indítási hozzáférés",
            "description": "Itt vannak a bejelentkezési adatok ahhoz az [aternos](https://aternos.org/servers) fiókhoz, amivel el tudjátok indítani a szervereket.\n**Felhasználónév:** pintermor9_BAccess\n**Jelszó:** access.aternos\n**Kérlek ne változtassad meg a jelszót!**",
        }
    )


SERVERS = {
    "pintermor9_SERVER_0.aternos.me:12599": {"edition": "crossplay"},
    "pintermor9_SERVER_1.aternos.me:30946": {"edition": "java"},
}

API_URL = "https://api.mcsrvstat.us/{0}2/{1}"


def is_online(server) -> bool:
    try:
        return int(server["players"]["max"]) > 1
    except:
        return False


class Guild__Minecraft(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.online = []
        logger.info("Loaded " + __name__)

    @commands.Cog.listener()
    async def on_ready_cogs(self):
        self.channel = self.bot.get_channel(
            self.bot.settings["data"]["minecraft"]["channel"]
        )
        self.message = await self.channel.fetch_message(
            self.bot.settings["data"]["minecraft"]["message"]
        )

        self.check_servers.start()

    @tasks.loop(minutes=5)
    async def check_servers(self):
        online = []
        for server in SERVERS.items():
            try:
                bedrock = "bedrock/" if server[1]["edition"] == "bedrock" else ""
                server = await self.bot.api.get(
                    API_URL.format(bedrock, server[0]), use_base=False, return_as="json"
                )
                if is_online(server):
                    online.append(server)
            except:
                continue

        for hostname in [server["hostname"] for server in online]:
            if not hostname in [server["hostname"] for server in self.online]:
                # * saját magam értesítése
                en = self.bot.get_user(761555679873597450)
                await en.send(f"{hostname} is online!")

                # * áron megspamelése
                aron = self.bot.get_user(735435854885158912)
                for _ in range(10):
                    await aron.send(f"{hostname} online van\nTe akartad")

        self.online = online

        await self.edit_server_list()

    async def edit_server_list(self):
        embed = discord.Embed(
            title="--              Online szerverek              --",
            timestamp=datetime.utcnow(),
            color=discord.Color.green(),
        )
        for server in self.online:
            embed.add_field(
                name=server["hostname"],
                value=f"{server['players']['online']}/{server['players']['max']}",
                inline=False,
            )
        if len(self.online) == 0:
            embed.color = discord.Color.red()
            embed.description = "Jelenleg egy szerver sincs online. :("

        await self.message.edit(embeds=[embed])

    @commands.command(name="refreshembeds", hidden=True)
    @commands.is_owner()
    async def _refreshembeds(self, ctx):
        for embed_name in Embeds.locations:
            embed = Embeds.__getattribute__(Embeds, embed_name)

            location = Embeds.locations[embed_name]
            channel = self.bot.get_channel(location[0])
            message = await channel.fetch_message(location[1])

            logger.info(message.embeds)


async def setup(bot):
    async def _setup():
        await bot.wait_until_ready()
        if not 954259643801157652 in [g.id for g in bot.guilds]:
            return
        await bot.add_cog(Guild__Minecraft(bot))

    bot.loop.create_task(_setup())
