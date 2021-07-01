from discord.ext import commands
from datetime import datetime
from time import time
import json
import asyncio
import requests


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
        if len(ctx.message.content[len(ctx.prefix + str(ctx.command)):].strip()) == 0:
            args = "no"
        else:
            args = f"`{ctx.message.content[len(ctx.prefix + str(ctx.command)):].strip()}`"

        requests.post("https://roboty-api.pintermor9.repl.co/logging/log", json={"channel": str(
            ctx.channel)[3:], "author": {ctx.author}, "command": ctx.command, "args": list(ctx.args)})


def setup(client):
    client.add_cog(Logging(client))
