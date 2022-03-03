from discord.ext import commands
import youtube_dl
import asyncio
import discord
import random

ytdl_format_options = {
    "format": "bestaudio/best",
    "outtmpl": "%(extractor)s-%(id)s-%(title)s.%(ext)s",
    "restrictfilenames": True,
    "noplaylist": True,
    "nocheckcertificate": True,
    "ignoreerrors": False,
    "logtostderr": False,
    "quiet": True,
    "no_warnings": True,
    "default_search": "auto",
    # Bind to ipv4 since ipv6 addresses cause issues at certain times
    "source_address": "0.0.0.0",
}

ffmpeg_options = {"options": "-vn"}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class Song:
    def __init__(self):
        self.embed = discord.Embed.from_dict({""})


class Queue(asyncio.Queue):
    def __init__(self):
        super().__init__(self, maxsize=100)

    def __len__(self):
        return self.qsize()

    def clear(self):
        self._queue.clear()

    def shuffle(self):
        random.shuffle(self._queue)


class MusicRewrite(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print('Loaded', __name__)

    @commands.command(name="join")
    async def _join(self, ctx):
        destination = ctx.author.voice.channel
        await destination.connect()

    @commands.command(name="leave")
    async def _leave(self, ctx):
        if ctx.author.voice.channel == ctx.voice_client.channel:
            await ctx.voice_client.disconnect()

    @commands.command(name="play")
    async def _play(self, ctx, query):
        if not ctx.voice_client:
            await ctx.invoke(self._join)

        async with ctx.typing():
            data = await self.bot.loop.run_in_executor(None, lambda: ytdl.extract_info(query, download=True, process=False))
            source = data  # TODO
            ctx.voice_client.play(
                source, after=lambda e: print(
                    f"Player error: {e}") if e else None
            )

    @_play.before_invoke
    @_join.before_invoke
    async def ensure_voice(self, ctx):
        if not ctx.author.voice or not ctx.author.voice.channel:
            raise commands.CommandError(
                'You are not connected to any voice channel.')

        if ctx.voice_client:
            if ctx.voice_client.channel != ctx.author.voice.channel:
                raise commands.CommandError(
                    'Bot is already in a voice channel.')


def setup(bot):
    bot.add_cog(MusicRewrite(bot))
