import ssl
from discord.ext import commands
from datetime import datetime
from time import time
import json
import asyncio
import aiohttp


class Logging(commands.Cog):
    def __init__(self, client):
        self.client = client
        print(f'Loaded', __name__)

    async def uptime_log(self):
        while True:
            with open("./data/uptime_ping.json", "w") as file:
                json.dump({"last_up": time()}, file)

            await asyncio.sleep(10)

    @commands.Cog.listener()
    async def on_command(self, ctx):
        args = [arg for index, arg in enumerate(ctx.message.content.split(' ')) if index != 0]

        data = {"channel": str(ctx.channel)[3:], "author": str(ctx.author), "command": str(ctx.command), "args": ' '.join(args)}

        async with aiohttp.ClientSession() as session:
            await session.post(f"https://roboty-api.pintermor9.repl.co/logging/log/?key={self.client.logging_apikey}", json=data, ssl=False)


def setup(client):
    client.add_cog(Logging(client))
