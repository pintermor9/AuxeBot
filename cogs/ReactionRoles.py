import discord
from discord.ext import commands
import json
import uuid
from asyncio import TimeoutError


class ReactionRoles(commands.Cog):
    def __init__(self, client):
        self.client = client
        print('Loaded', __name__)

    @commands.Cog.listener()
    async def on_ready(self):
        self.client.reaction_roles_channel = self.client.get_channel(
            self.client.data["reaction_roles"]["channel"])
        self.client.reaction_roles_message = await self.client.reaction_roles_channel.fetch_message(
            self.client.data["reaction_roles"]["message"])
        self.client.reaction_roles_data = json.loads(
            self.client.reaction_roles_message.content)
        print(__name__+": "+str(self.client.reaction_roles_data))

        # ? delete guilds with no RRs from dictionary (cleanup)
        self.client.reaction_roles_data = {
            guild: data for guild, data in self.client.reaction_roles_data.items() if data != []}
        await self.save_reaction_roles()

    async def save_reaction_roles(self):
        await self.client.reaction_roles_message.edit(content=json.dumps(self.client.reaction_roles_data, indent=2))

    def parse_reaction_payload(self, payload: discord.RawReactionActionEvent):
        guild_id = payload.guild_id
        data = self.client.reaction_roles_data.get(str(guild_id), None)
        if data is not None:
            for rr in data:
                emote = rr.get("emote")
                if int(payload.message_id) == int(rr.get("messageID")):
                    if int(payload.channel_id) == int(rr.get("channelID")):
                        if str(payload.emoji) == str(emote):
                            guild = self.client.get_guild(guild_id)
                            role = guild.get_role(int(rr.get("roleID")))
                            user = guild.get_member(int(payload.user_id))
                            if user != self.client.user:
                                return role, user
        return None, None

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        role, user = self.parse_reaction_payload(payload)
        if role is not None and user is not None and user is not self.client.user:
            await user.add_roles(role, reason="ReactionRole")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        role, user = self.parse_reaction_payload(payload)
        if role is not None and user is not None and user is not self.client.user:
            await user.remove_roles(role, reason="ReactionRole")

    @commands.has_permissions(manage_channels=True, manage_roles=True)
    @commands.command(description="Creates a new reaction role.")
    async def reaction(self, ctx, emote, role: discord.Role, channel: discord.TextChannel, title, message):
        """Creates a new reaction role. The bot will send an embed message, wich will be the base of the reaction role.
        **Parameters:**
        `emote`: The emoji that users need to react in order to get the role.
        `role`: A role that users get.
        `channel`: The channel that the embed gets sent in. This can be the channels mention, name or id.
        `title`: Title of the embed.
        `message`: Description of the embed.
        """
        embed = discord.Embed(title=title, description=message)
        msg = await channel.send(embed=embed)
        await msg.add_reaction(emote)
        self.add_reaction(ctx.guild.id, emote, role.id, channel.id, msg.id)
        await self.save_reaction_roles()

    @commands.has_permissions(manage_channels=True, manage_roles=True)
    @commands.group(invoke_without_command=True, description="Lists the reaction roles in the current guild.")
    async def reactions(self, ctx):
        guild_id = ctx.guild.id
        data = self.client.reaction_roles_data.get(str(guild_id), None)
        embed = discord.Embed(title="Reaction Roles")
        if data == None or data == []:
            embed.description = "There are no reaction roles set up right now."
        else:
            for index, rr in enumerate(data):
                emote = rr.get("emote")
                role_id = rr.get("roleID")
                role = ctx.guild.get_role(role_id)
                channel_id = rr.get("channelID")
                message_id = rr.get("messageID")
                embed.add_field(
                    name=index,
                    value=f"{emote} - @{role} - [message](https://www.discord.com/channels/{guild_id}/{channel_id}/{message_id})",
                    inline=False,
                )
        await ctx.send(embed=embed)

    @commands.has_permissions(manage_channels=True, manage_roles=True)
    @reactions.command(description="Creates a new reaction role.")
    async def add(self, ctx, emote, role: discord.Role, channel: discord.TextChannel, message_id):
        """Creates a new reaction role for an existing message.
        **Parameters:**
        `emote`: The emoji that users need to react in order to get the role.
        `role`: A role that users get.
        `channel`: The channel that the embed gets sent in. This can be the channels mention, name or id.
        `message_id`: This is the id of the message that will be the base of the reaction role.
        """
        msg = await channel.fetch_message(int(message_id))
        await msg.add_reaction(emote)
        self.add_reaction(ctx.guild.id, emote, role.id, channel.id, message_id)
        await self.save_reaction_roles()

    @commands.has_permissions(manage_channels=True)
    @reactions.command(description="Removes an existing reaction role.")
    async def remove(self, ctx, index: int):
        """Removes an existing reaction role in the current guild. It takes the `index` of the reaction role, which you can see by invoking `reactions`."""
        guild_id = ctx.guild.id
        data = self.client.reaction_roles_data.get(str(guild_id), None)
        embed = discord.Embed(title=f"Remove Reaction Role {index}")
        rr = None
        if data is None:
            embed.description = "Given Reaction Role was not found."
        else:
            embed.description = (
                "Do you wish to remove the reaction role below? Please react with 🗑️."
            )
            rr = data[index]
            emote = rr.get("emote")
            role_id = rr.get("roleID")
            role = ctx.guild.get_role(role_id)
            channel_id = rr.get("channelID")
            message_id = rr.get("messageID")
            _id = rr.get("id")
            embed.set_footer(text=_id)
            embed.add_field(
                name=index,
                value=f"{emote} - @{role} - [message](https://www.discord.com/channels/{guild_id}/{channel_id}/{message_id})",
                inline=False,
            )
        msg = await ctx.send(embed=embed)
        if rr is not None:
            await msg.add_reaction("🗑️")

            def check(reaction, user):
                return (
                    reaction.message.id == msg.id
                    and user == ctx.message.author
                    and str(reaction.emoji) == "🗑️"
                )
            try:
                reaction, user = await self.client.wait_for("reaction_add", check=check, timeout=15)
                data.remove(rr)
                embed = discord.Embed(title="Ok. Deleted.🗑️")
            except TimeoutError:
                embed = discord.Embed(title="Timed out...")
            finally:
                await msg.clear_reactions()
                await msg.edit(embed=embed)
            self.client.reaction_roles_data[str(guild_id)] = data
            await self.save_reaction_roles()

    def add_reaction(self, guild_id, emote: discord.Emoji, role_id, channel_id, message_id):
        if not str(guild_id) in self.client.reaction_roles_data:
            self.client.reaction_roles_data[str(guild_id)] = []
        self.client.reaction_roles_data[str(guild_id)].append(
            {
                "id": str(uuid.uuid4()),
                "emote": emote,
                "roleID": int(role_id),
                "channelID": int(channel_id),
                "messageID": int(message_id),
            }
        )


def setup(client):
    client.add_cog(ReactionRoles(client))
