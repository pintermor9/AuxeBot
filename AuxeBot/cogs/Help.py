import discord
from Utils import Paginator
from discord.ext import commands


class HelpCommand(commands.HelpCommand):
    def __init__(self, **options):
        super().__init__(**options)

    async def send_bot_help(self, _mapping):
        bot = self.context.bot
        embeds = []
        cogs = [cog for cog in bot.cogs.values() if len([command for command in cog.get_commands(
        ) if not command.hidden]) > 0 and cog.qualified_name not in bot.hidden_cogs]
        max_page = len(cogs)
        for cog in cogs:
            embed = discord.Embed(
                title=f"Documentation for `{cog.qualified_name}`", description=f"All cogs: {', '.join([cog.qualified_name for cog in cogs])}")
            for command in cog.get_commands():
                if command.hidden:
                    continue
                try:
                    children = command.commands
                except:
                    children = None
                if command.brief:
                    description = command.brief
                elif command.description:
                    description = command.description
                else:
                    description = "This command does not have any description yet."
                children = f"\n**Children:** {', '.join([child.name for child in children])}" if children != None else ""
                embed.add_field(name=command.name,
                                value=f"{description}{children}")
                embed.set_footer(text=f"Page {(cogs.index(cog))+1}/{max_page}")
            embeds.append(embed)
        paginator = Paginator(self.context, embeds)
        await paginator.run()

    async def send_command_help(self, command):
        if command.parent:
            parent = command.parent.name + " "
        else:
            parent = ""
        if command.help:
            description = command.help
        elif command.description:
            description = command.description
        elif command.brief:
            description = command.brief
        else:
            description = "This command does not have any description yet."
        embed = discord.Embed(
            title=f"Documentation for `{parent}{command.name}`", description=description)
        if command.aliases != []:
            embed.add_field(name="Aliases:", value=", ".join(command.aliases))
        embed.add_field(
            name="Usage", value=f"`{parent}{command.name} {command.signature.replace('=', ' = ')}".strip()+"`", inline=False)
        embed.set_footer(
            text="`< argument > required, [ argument = default ] optional`")
        return await self.get_destination().send(embed=embed)

    async def send_group_help(self, group):
        if group.help:
            description = group.help
        elif group.description:
            description = group.description
        elif group.brief:
            description = group.brief
        else:
            description = "This command does not have any description yet."
        embed = discord.Embed(
            title=f"Documentation for `{group.name}`", description=description)
        children = ""
        for child in group.commands:
            if child.brief:
                child_description = group.brief
            elif child.description:
                child_description = child.description
            else:
                child_description = "This command does not have any description yet."
            children += f"> **{child.name}:** *{child_description}*\n> \u2800Usage: `{group.name} {child.name} {child.signature.replace('=', ' = ')}".strip(
            )+"`\n"
        embed.add_field(name=f"Child commands:", value=children)
        embed.set_footer(text="< > required, [ ] optional argument")
        return await self.get_destination().send(embed=embed)

    async def send_cog_help(self, cog):
        embed = discord.Embed(
            title=f"Documentation for `{cog.qualified_name}`")
        for command in cog.get_commands():
            if command.hidden:
                continue
            try:
                children = command.commands
            except:
                children = None
            if command.brief:
                description = command.brief
            elif command.description:
                description = command.description
            else:
                description = "This command does not have any description yet."
            children = f"\n**Children:** {', '.join([child.name for child in children])}" if children != None else ""
            embed.add_field(name=command.name,
                            value=f"{description}{children}")
        await self.get_destination().send(embed=embed)


def setup(bot):
    bot.help_command = HelpCommand()
