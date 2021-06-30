import discord
from discord.ext import commands


class Moderation(commands.Cog):
	def __init__(self, client):
		self.client = client
		print(f'Loaded', __name__)

	def is_owner(self, ctx):
		def predicate(ctx):
			return ctx.message.author.id in self.owner_IDs

		return commands.check(predicate)

	@commands.command()
	async def ping(self, ctx):
		await ctx.send(f'Pong! {round(self.client.latency * 1000)}ms')

	@commands.command()
	async def info(self, ctx):
		embed = discord.Embed(
		    title="Info about the bot",
		    description="Source code: replit.com/@pintermor9/Roboty")
		await ctx.send(embed=embed)

	@commands.command(aliases=['clear', 'cls'])
	@commands.has_permissions(manage_messages=True)
	async def purge(self, ctx, amount: int = None):
		if amount == None:
			await ctx.send('Please set an amount!')
		else:
			await ctx.channel.purge(limit=(amount + 1))

	@commands.command()
	@commands.check(is_owner)
	async def logout(self, ctx):
		await ctx.send('Bye! :wave:')
		await self.client.change_presence(
		    status=discord.Status.do_not_disturb,
		    activity=discord.Game("Shutting down..."))
		await self.client.logout()

	@commands.command()
	async def getctx(self, ctx):
		await ctx.message.delete()
		print(ctx.__dict__)
		await ctx.send('Context printed to console.', delete_after=5)

	@commands.command()
	async def test(self, ctx, USER_ID):
		a = self.client.get_user(int(USER_ID))
		print(a)


def setup(client):
	client.add_cog(Moderation(client))
