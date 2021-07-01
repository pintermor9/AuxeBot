from discord.ext import commands
from datetime import datetime
from time import time
import json
import asyncio


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
    async def on_ready(self):
        with open("./data/uptime_ping.json") as file:
            last_up = json.load(file)["last_up"]
        
        

        with open("./data/log.log", "a") as file:
            file.write(
                f"\n\n-----\n{str(datetime.now())[:-7]}: Bot started after {round(time() - last_up)} seconds of downtime.\n\n"
            )

        await self.uptime_log()

    @commands.Cog.listener()
    async def on_command(self, ctx):
        if len(ctx.message.content[len(ctx.prefix + str(ctx.command)):].strip()) == 0:
            args = "no"
        else:
            args = f"`{ctx.message.content[len(ctx.prefix + str(ctx.command)):].strip()}`"
    
        with open("./data/log.log", "a") as file:
            file.write(
                f"{str(datetime.now())[:-7]}: {ctx.author} invoked `{ctx.command}` command with {args} arguments in `#{str(ctx.channel)[3:]}`.\n"
            )


def setup(client):
    client.add_cog(Logging(client))
