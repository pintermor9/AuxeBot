import discord
import logging
import random
import disutils
from discord.ext import commands
from discord.ext.commands.errors import BadArgument

logger = logging.getLogger(__name__)


class Music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.music = disutils.Music()
        logger.info("Loaded " + __name__)

    @commands.command()
    async def join(self, ctx):
        """Joins a voice channel."""
        try:
            await ctx.author.voice.channel.connect()  # Joins author's voice channel
        except AttributeError:
            raise Music.NotConnectedToVoice("You're not connected to a voice channel.")

    @commands.command()
    async def leave(self, ctx):
        """Clears the queue and leaves the voice channel."""
        player = self.music.get_player(ctx)
        await player.stop()
        await ctx.voice_client.disconnect()

    @commands.command()
    async def play(self, ctx, *, url):
        """Plays a song.

        If there are songs in the queue, this will be queued until the
        other songs finished playing.

        This command automatically searches from various sites if no URL is provided.
        A list of these sites can be found here: https://rg3.github.io/youtube-dl/supportedsites.html
        """
        async with ctx.typing():
            if not ctx.voice_client:
                await ctx.invoke(self.join)
            player = self.music.get_player(ctx)
            if not player.is_playing:
                await player.queue(url)
                song = await player.play()
                await ctx.send(f"Playing {song.title}")
            else:
                song = await player.queue(url)
                await ctx.send(f"Queued {song.title}")

    @commands.command()
    async def pause(self, ctx):
        """Pauses the currently playing song."""
        player = self.music.get_player(ctx)
        song = await player.pause()
        await ctx.send(f"Paused {song.title}")

    @commands.command()
    async def resume(self, ctx):
        """Resumes a currently paused song."""
        player = self.music.get_player(ctx)
        song = await player.resume()
        await ctx.send(f"Resumed {song.title}")

    @commands.command()
    async def stop(self, ctx):
        """Stops playing song and clears the queue."""
        player = self.music.get_player(ctx)
        await player.stop()
        await ctx.send("Stopped")

    @commands.command()
    async def loop(self, ctx):
        """Loops the currently playing song.
        Invoke this command again to unloop the song."""
        player = self.music.get_player(ctx)
        song = await player.toggle_song_loop()
        if song.is_looping:
            await ctx.send(f"Enabled loop for {song.title}")
        else:
            await ctx.send(f"Disabled loop for {song.title}")

    @commands.command()
    async def queue(self, ctx):
        """Shows the player's queue."""
        player = self.music.get_player(ctx)
        text = ""
        for i, song in enumerate([song.title for song in player.song_queue]):
            text += f"`{i+1}.` {song}\n"
        await ctx.send(text)

    @commands.command()
    async def now(self, ctx):
        """Displays the currently playing song."""
        player = self.music.get_player(ctx)
        song = player.now_playing()
        await ctx.send(song.title)

    @commands.command()
    async def skip(self, ctx):
        """Skips the currently playing song."""
        player = self.music.get_player(ctx)
        data = await player.skip(force=True)
        if data[1] is not None: 
            await ctx.send(f"Skipped from {data[0].title} to {data[1].title}")
        else:
            await ctx.send(f"Skipped {data[0].title}")

    @commands.command(aliases=["vol"])
    async def volume(self, ctx, vol: int = None):
        """Sets the volume of the player. If no volume is provided, it will return the current volume."""
        player = self.music.get_player(ctx)
        if vol is None:
            return await ctx.send(f"Volume is {player.volume * 100}%")	
        if vol > 100 or vol < 0:
            raise BadArgument("`vol` must be between 0 and 100")
        else:
            song, volume = await player.change_volume(float(vol) / 100)
            await ctx.send(f"Changed volume for {song.title} to {vol}%")

    @commands.command()
    async def remove(self, ctx, index):
        """Removes a song from the queue at a given index."""
        player = self.music.get_player(ctx)
        song = await player.remove_from_queue(int(index-1))
        await ctx.send(f"Removed {song.title} from queue")

    @commands.command()
    async def shuffle(self, ctx):
        """Shuffles the queue"""
        player = self.music.get_player(ctx)
        player.shuffle_queue()
        await ctx.send("Shuffled!")


def setup(bot):
    bot.add_cog(Music(bot))
