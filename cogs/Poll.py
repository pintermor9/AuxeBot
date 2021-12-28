import json
import discord
from time import time
from discord.ext import commands
from discord.ext.commands.errors import ArgumentParsingError


class Poll(commands.Cog):
    def __init__(self, client):
        self.client = client
        print(f'Loaded', __name__)

    @commands.Cog.listener()
    async def on_ready(self):
        self.client.poll_channel = self.client.get_channel(
            self.client.data["poll"]["channel"])
        self.client.poll_message = await self.client.poll_channel.fetch_message(
            self.client.data["poll"]["message"])
        self.client.poll_data = json.loads(
            self.client.poll_message.content)
        print(__name__+": "+str(self.client.poll_data))

    async def save_poll(self):
        await self.client.poll_message.edit(content=json.dumps(self.client.poll_data, indent=2))

    """poll_data = [{"channel": "int", "message": "int", "expires": "time.time()", "choices": [
        {"emote": "emoji", "name": "1. válasz"}]}]"""

    @commands.command(name="poll", description="Creates a poll.")
    async def _poll(self, ctx, lenght, choices, message):
        """
        Creates a poll, with the polls base being an embed.
        **Parameters:**
        `lenght`: The time that the poll should last **in seconds**. (`WIP`)
        `choiches`: The possible choiches. It needs to be inside quotes, every choice needs to have a an emoji and a name (separated with colons) and choiches need to be separated with a comma.
            > eg. "👍:choice1,👎:choice2"
        `message`: The sent embeds description. This also needs to be inside quotes.
        """
        try:
            choices = [choice.strip() for choice in choices.split(",")]
            _choices = []
            for choice in choices:
                emote, name = choice.split(":")
                _choices.append({emote.strip(): name.strip()})
            choices = _choices
        except:
            raise ArgumentParsingError(
                "An error ocurred while parsing argument: `choices`")

        description = message + "\n**Choices:**"
        for choice in choices:
            description += f"\n**{list(choice.keys())[0]}:** {list(choice.values())[0]}"

        embed = discord.Embed(
            title=f"Poll: by {ctx.author.name + '#' + ctx.author.discriminator}", description=description)

        msg = await ctx.send(embed=embed)

        for choice in choices:
            await msg.add_reaction(list(choice.keys())[0])

        expires = round(time()) + int(lenght)
        self.client.poll_data.append(
            {"channel": msg.channel.id, "message": msg.id, "expires": expires, "choices": choices})

        await self.save_poll()

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if self.client.user == payload.member:
            return
        channels = [poll["channel"] for poll in self.client.poll_data]
        if payload.channel_id not in channels:
            return
        messages = [poll["message"] for poll in self.client.poll_data]
        if payload.message_id not in messages:
            return
        poll = next(poll for poll in self.client.poll_data if poll["channel"] ==
                    payload.channel_id and poll["message"] == payload.message_id)
        if str(payload.emoji) not in [list(choice.keys())[0] for choice in poll["choices"]]:
            return
        channel = self.client.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)

        voted_users = []
        for reaction in message.reactions:
            users = await reaction.users().flatten()
            users.pop(users.index(self.client.user))
            voted_users.extend(users)

        if voted_users.count(payload.member) > 1:
            await message.remove_reaction(payload.emoji, payload.member)
            await message.channel.send(f"{payload.member.mention} You can't vote for 2 choices!", reference=message, delete_after=5)


"""
[
    {
        "channel": "int",
        "message": "int",
        "expires": "time.time()",
        "choices": [
            {
                "emote": "name"
            }
        ]
    }
]
"""


def setup(client):
    print("                              !!! MAKE POLLS END !!!\n                           Temporarily disabled Poll.py")
    # client.add_cog(Poll(client))
