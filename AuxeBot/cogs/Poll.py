import logging
import discord
import datetime
from time import time
from discord.ext import commands, tasks
from discord.ext.commands.errors import ArgumentParsingError

logger = logging.getLogger(__name__)


class Poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        logger.info("Loaded " + __name__)

    @commands.Cog.listener()
    async def on_ready_cogs(self):
        self.expiry_check.start()

    @commands.command(name="poll", description="Creates a poll.")
    async def _poll(self, ctx, lenght: int, choices, message):
        """
        Creates a poll, with the polls base being an embed.
        **Parameters:**
        `lenght`: The time that the poll should last **in minutes**. (`WIP`)
        `choiches`: The possible choiches. It needs to be inside quotes, every choice needs to have a an emoji and a name (separated with colons) and choiches need to be separated with a comma.
            > eg. "👍:choice1,👎:choice2"
        `message`: The sent embeds description. This also needs to be inside quotes.
        """
        try:
            choices = [choice.strip() for choice in choices.split(",")]
            _choices = {}
            for choice in choices:
                emote, name = choice.split(":")
                _choices.update({emote.strip(): name.strip()})
            choices = _choices
        except:
            raise ArgumentParsingError(
                "An error ocurred while parsing argument: `choices`"
            )

        description = message + "\n**Choices:**"
        for choice in choices:
            description += f"\n**{choice}:** {choices[choice]}"
        embed = discord.Embed(
            title=f"Poll by {ctx.author.name + '#' + ctx.author.discriminator}:",
            description=description,
        )
        embed.set_footer(text="Ends: ")
        embed.timestamp = datetime.datetime.now() + datetime.timedelta(minutes=lenght)
        msg = await ctx.send(embed=embed)

        for choice in choices:
            await msg.add_reaction(choice)

        expires = round(time()) + (lenght * 60)
        poll = {
            "channel": msg.channel.id,
            "message": msg.id,
            "expires": expires,
            "choices": choices,
        }
        self.bot.data["poll"].append(poll)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if self.bot.user == payload.member:
            return
        channels = [poll["channel"] for poll in self.bot.data["poll"]]
        if payload.channel_id not in channels:
            return
        messages = [poll["message"] for poll in self.bot.data["poll"]]
        if payload.message_id not in messages:
            return
        poll = next(
            poll
            for poll in self.bot.data["poll"]
            if poll["channel"] == payload.channel_id
            and poll["message"] == payload.message_id
        )
        if str(payload.emoji) not in [choice for choice in poll["choices"]]:
            return
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)

        voted_users = []
        for reaction in message.reactions:
            users = await reaction.users().flatten()
            users.pop(users.index(self.bot.user))
            voted_users.extend(users)

        if voted_users.count(payload.member) > 1:
            await message.remove_reaction(payload.emoji, payload.member)
            await message.channel.send(
                f"{payload.member.mention} You can't vote for 2 choices!",
                reference=message,
                delete_after=5,
            )

    async def end_poll(self, poll_index: int):
        poll = self.bot.data["poll"][poll_index]
        channel = self.bot.get_channel(poll["channel"])
        message = await channel.fetch_message(poll["message"])

        votes = {}
        for reaction in message.reactions:
            users = await reaction.users().flatten()
            try:
                users.pop(users.index(self.bot.user))
            finally:
                votes.update({str(reaction): users})

        embed = discord.Embed(
            title=message.embeds[0].title.replace("Poll ", "Poll results "),
            description=message.embeds[0].description + "\n\n**Results:**",
        )
        for vote in votes.items():
            embed.add_field(name=poll["choices"][vote[0]], value=len(vote[1]))
        await message.edit(embed=embed)
        await message.clear_reactions()

        self.bot.data["poll"].pop(self.bot.data["poll"].index(poll))

    @tasks.loop(seconds=10)
    async def expiry_check(self):
        try:
            expired = list(
                filter(
                    lambda p: p["expires"] <= int(
                        round(time())), self.bot.data["poll"]
                )
            )
            for poll in expired:
                await self.end_poll(self.bot.data["poll"].index(poll))
        except:
            pass  # It'll prolly work 10 seconds later XD


async def setup(bot):
    await bot.add_cog(Poll(bot))
