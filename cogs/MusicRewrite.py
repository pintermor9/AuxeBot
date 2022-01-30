import discord
import youtube_dl
from discord.ext import commands

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
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
        ctx.voice_client.play(
            source, after=lambda e: print(f"Player error: {e}") if e else None
        )


def setup(bot):
    bot.add_cog(MusicRewrite(bot))
