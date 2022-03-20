import json
import discord
from io import StringIO
from asyncio import TimeoutError
from typing import List, Literal, Union


class Paginator:  # TODO NEEDS REWRITE WITH COMPONENTS
    def __init__(self, ctx, embeds):
        self.ctx = ctx
        self.client = ctx.bot
        self.embeds = embeds

    async def run(self):
        embeds = self.embeds
        message = await self.ctx.send("\u2800")
        current_page = 0
        EMOJIS = ('⏮️', '⏪', '⏹️', '⏩', '⏭️')
        for emoji in EMOJIS:
            await message.add_reaction(emoji)

        def check(reaction, user):
            return user == self.ctx.author and reaction.message.id == message.id and str(reaction.emoji) in EMOJIS
        await message.edit(embed=embeds[current_page])
        while True:
            try:
                reaction, user = await self.client.wait_for("reaction_add", check=check, timeout=30)
                await reaction.remove(user)
                if str(reaction.emoji) == '⏮️':
                    current_page = 0
                if str(reaction.emoji) == '⏪':
                    current_page -= 1
                if str(reaction.emoji) == '⏹️':
                    return await message.clear_reactions()
                if str(reaction.emoji) == '⏩':
                    current_page += 1
                if str(reaction.emoji) == '⏭️':
                    current_page = len(embeds) - 1

                if current_page > len(embeds) - 1:
                    current_page -= 1
                if current_page < 0:
                    current_page = 0

                await message.edit(embed=embeds[current_page])
            except TimeoutError:
                try:
                    return await message.clear_reactions()
                except:
                    pass


class Data:
    @staticmethod
    async def load(client, message: Union[discord.Message, List[int]]):
        if type(message) == list:
            _channel = client.get_channel(message[0])
            message = await _channel.fetch_message(message[1])
        file_message = await message.channel.fetch_message(int(message.content))
        bytes = await file_message.attachments[0].read()
        return json.loads(bytes)

    @staticmethod
    async def dump(client, data, message: Union[discord.Message, List[int]]):
        if type(message) == list:
            _channel = client.get_channel(message[0])
            message = await _channel.fetch_message(message[1])
        if type(data) == dict:
            data = json.dumps(data, indent=4)
        old_file_message = await message.channel.fetch_message(int(message.content))
        file = discord.File(StringIO(data), filename="data.json")
        file_message = await message.channel.send(file=file)
        await message.edit(content=str(file_message.id))
        await old_file_message.delete()


class Api:
    def __init__(self, bot, session):
        self.session = session
        self.bot = bot
        self.base_url = bot.settings["api_base_url"]

    async def get(self, url, use_base=True, return_as: Literal["text", "json"] = None):
        _url = self.base_url + url if use_base else url
        async with self.session.get(_url) as resp:
            if return_as == "json" or resp.content_type == "application/json":
                return await resp.json()
            elif return_as == "text" or resp.content_type.startswith("text"):
                return await resp.text()
            else:
                return await resp.read()

    async def post(self, url, *, data, use_base=True, return_as: Literal["text", "json"] = None):
        _url = self.base_url + url if use_base else url
        async with self.session.post(_url, data=data) as resp:
            if return_as == "json" or resp.content_type == "application/json":
                return await resp.json()
            elif return_as == "text" or resp.content_type.startswith("text"):
                return await resp.text()
            else:
                return await resp.read()
