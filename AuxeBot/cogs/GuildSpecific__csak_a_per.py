import logging
from discord.ext import commands

logger = logging.getLogger(__name__)


class GuildSpecific__csak_a_per(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        logger.info("Loaded " + __name__)

    @commands.Cog.listener()
    async def on_message(self, message):
        # auto-shopthreading
        if message.channel.id == 920590116710412298 and message.author != self.bot.user:
            if message.attachments == []:
                await message.channel.send(
                    "Ide csak a store-odat küldjed. Kell lennie egy fényképnek csatolva.",
                    delete_after=10,
                )
                return await message.delete()
            name = f"{message.author.name}`s store"
            to_delete = [
                thread
                for thread in message.channel.threads
                if thread.name == name and not thread.archived
            ]
            for t in to_delete:
                await t.archive()
            await message.channel.create_thread(name=name, message=message)

        # valorant twitter news
        if message.channel.id == 947548279531524186:
            channel = self.bot.get_channel(928696145440550942)
            await channel.send(
                message.content,
                embeds=message.embeds,
                files=[
                    await attachment.to_file() for attachment in message.attachments
                ],
            )


async def setup(bot):
    await bot.wait_for("connect")
    if not 954259643801157652 in [g.id for g in bot.guilds]:
        return
    await bot.add_cog(GuildSpecific__csak_a_per(bot))
