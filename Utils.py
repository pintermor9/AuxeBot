from asyncio import TimeoutError
import discord


class Paginator:
    def __init__(self, ctx, embeds):
        self.ctx = ctx
        self.client = ctx.bot
        self.embeds = embeds

    async def run(self):
        embeds = self.embeds
        message = await self.ctx.send(embed=discord.Embed(title="\u2800"))
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
                return await message.clear_reactions()
