import discord, random
from discord.ext import commands
import DiscordUtils


class Music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.music = DiscordUtils.Music()
        print(f'Loaded', __name__)

    @commands.command()
    async def join(self, ctx):
        """Joins a voice channel."""
        await ctx.author.voice.channel.connect() # Joins author's voice channel

    @commands.command()
    async def leave(self, ctx):
        """Clears the queue and leaves the voice channel."""
        await ctx.invoke(self.stop)
        await ctx.voice_client.disconnect()

    @commands.command()
    async def play(self, ctx, *, url):
        """Plays a song.

        If there are songs in the queue, this will be queued until the
        other songs finished playing.

        This command automatically searches from various sites if no URL is provided.
        A list of these sites can be found here: https://rg3.github.io/youtube-dl/supportedsites.html
        """
        player = music.get_player(guild_id=ctx.guild.id)
        if not player:
            player = music.create_player(ctx, ffmpeg_error_betterfix=True)
        if not ctx.voice_client.is_playing():
            await player.queue(url, search=True)
            song = await player.play()
            await ctx.send(f"Playing {song.name}")
        else:
            song = await player.queue(url, search=True)
            await ctx.send(f"Queued {song.name}")

    @commands.command()
    async def pause(self, ctx):
        """Pauses the currently playing song."""
        player = music.get_player(guild_id=ctx.guild.id)
        song = await player.pause()
        await ctx.send(f"Paused {song.name}")

    @commands.command()
    async def resume(self, ctx):
        """Resumes a currently paused song."""
        player = music.get_player(guild_id=ctx.guild.id)
        song = await player.resume()
        await ctx.send(f"Resumed {song.name}")

    @commands.command()
    async def stop(self, ctx):
        """Stops playing song and clears the queue."""
        player = music.get_player(guild_id=ctx.guild.id)
        await player.stop()
        await ctx.send("Stopped")

    @commands.command()
    async def loop(self, ctx):
        """Loops the currently playing song.
        Invoke this command again to unloop the song."""
        player = music.get_player(guild_id=ctx.guild.id)
        song = await player.toggle_song_loop()
        if song.is_looping:
            await ctx.send(f"Enabled loop for {song.name}")
        else:
            await ctx.send(f"Disabled loop for {song.name}")

    @commands.command()
    async def queue(self, ctx):
        """Shows the player's queue."""
        player = music.get_player(guild_id=ctx.guild.id)
        await ctx.send(f"{', '.join([song.name for song in player.current_queue()])}")

    @commands.command()
    async def now(self, ctx):
        """Displays the currently playing song."""
        player = music.get_player(guild_id=ctx.guild.id)
        song = player.now_playing()
        await ctx.send(song.name)

    @commands.command()
    async def skip(self, ctx):
        """Skips the currently playing song."""
        player = music.get_player(guild_id=ctx.guild.id)
        data = await player.skip(force=True)
        if len(data) == 2:
            await ctx.send(f"Skipped from {data[0].name} to {data[1].name}")
        else:
            await ctx.send(f"Skipped {data[0].name}")

    @commands.command()
    async def volume(self, ctx, vol):
        """Sets the volume of the player."""
        player = music.get_player(guild_id=ctx.guild.id)
        song, volume = await player.change_volume(float(vol) / 100) # volume should be a float between 0 to 1
        await ctx.send(f"Changed volume for {song.name} to {volume*100}%")

    @commands.command()
    async def remove(self, ctx, index):
        """Removes a song from the queue at a given index."""
        player = music.get_player(guild_id=ctx.guild.id)
        song = await player.remove_from_queue(int(index))
        await ctx.send(f"Removed {song.name} from queue")
    
    @commands.command()
    async def shuffle(self, ctx, index):
        random.shuffle(self.music.queue[ctx.guild.id])
        await ctx.send("Shuffled!")



def setup(bot):
    bot.add_cog(Music(bot))
