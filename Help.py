import discord
from discord import embeds
from discord.ext import commands


class HelpCommand(commands.HelpCommand):
    def __init__(self, **options):
        super().__init__(**options)

    async def send_bot_help(self, mapping):
        client = self.context.bot
        embed = discord.Embed(title="Help cmd")
        for cog in mapping:
            if cog == None:
                continue
            cog = client.get_cog(cog.qualified_name)
            if cog.get_commands() == []:
                continue
            value = ""
            for command in cog.get_commands():
                if command.hidden:
                    continue
                try:
                    bold = "**" if len(command.commands) > 0 else ""
                except:
                    bold = ""
                value += f"{bold}{command.name}{bold}, "
            embed.add_field(name=cog.qualified_name,
                            value=value[0:-2])

        await self.get_destination().send(embed=embed)

    async def send_command_help(self, command):
        return await self.get_destination().send(embed=self.context.bot.WorkInProgressEmbed)

    async def send_group_help(self, group):
        return await self.get_destination().send(embed=self.context.bot.WorkInProgressEmbed)

    async def send_cog_help(self, cog):
        helpText = ""
        embed = discord.Embed(
            title="Help commands!", color=0x012345
        )
        for command in cog.walk_commands():
            if command.hidden:
                continue

            elif command.parent != None:
                continue

            helpText += f"```{command.name}```\n**{command.description}**\n\n"

            if len(command.aliases) > 0:
                helpText += f'**Aliases: ** `{", ".join(command.aliases)}`'
            helpText += '\n'

            helpText += f'**Format:** `{self.context.bot.prefix}{command.name} {command.signature if command.signature is not None else ""}`\n\n'
        embed.description = helpText
        await self.get_destination().send(embed=embed)
