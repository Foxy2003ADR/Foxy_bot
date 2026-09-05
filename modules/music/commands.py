import discord
from discord.ext import commands

from .player import MusicPlayer
from .queue import get_queue
from .sources import search_youtube


class MusicCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.player = MusicPlayer(bot)

    async def ensure_voice(self, ctx):
        """Comprueba que el usuario esté en un canal de voz y conecta a Foxy."""

        if not ctx.author.voice or not ctx.author.voice.channel:
            await ctx.send("❌ Tienes que estar en un canal de voz primero.")
            return None

        channel = ctx.author.voice.channel
        voice = ctx.guild.voice_client

        try:
            if voice is None:
                voice = await channel.connect()
            elif voice.channel != channel:
                await voice.move_to(channel)

            return voice

        except Exception as error:
            print(f"[Music] Error conectando al canal de voz: {error}")
            await ctx.send(
                f"❌ No pude entrar al canal de voz: `{error}`"
            )
            return None

    @commands.command(name="p")
    async def play(self, ctx, *, query: str = None):
        """Busca y reproduce una canción."""

        if not query:
            await ctx.send("❌ Usa: `!p nombre de la canción`")
            return

        # Primero conectar al canal de voz
        voice = await self.ensure_voice(ctx)

        if voice is None:
            return

        await ctx.send(f"🔎 Buscando **{query}**...")

        try:
            song = await search_youtube(
                query,
                requester=ctx.author.display_name
            )

        except Exception as error:
            print(f"[Music] Error buscando canción: {error}")
            await ctx.send(
                f"❌ No pude encontrar la canción: `{error}`"
            )
            return

        queue = get_queue(ctx.guild.id)

        was_empty = len(queue.songs) == 0

        queue.add(song)

        # Si es la primera canción, fijamos el índice actual
        if was_empty:
            queue.current_index = 0

        await ctx.send(
            f"🎵 Añadida a la cola: **{song.title}**\n"
            f"🔗 {song.webpage_url}"
        )

        # Reproducir automáticamente si estaba parado
        if was_empty and not voice.is_playing():
            await self.player.play_current(ctx.guild)

    @commands.command(name="a")
    async def actual(self, ctx):
        """Muestra la canción actual."""

        queue = get_queue(ctx.guild.id)
        song = queue.current

        if song is None:
            await ctx.send("🎵 No hay ninguna canción reproduciéndose.")
            return

        await ctx.send(
            f"🎶 **Ahora sonando:** {song.title}\n"
            f"🔗 {song.webpage_url}"
        )

    @commands.command(name="n")
    async def next_song(self, ctx):
        """Pasa a la siguiente canción."""

        voice = ctx.guild.voice_client

        if voice is None:
            await ctx.send("❌ No estoy en ningún canal de voz.")
            return

        queue = get_queue(ctx.guild.id)

        if not queue.has_next():
            await ctx.send("⏭️ No hay más canciones en la cola.")
            return

        # Avanzar nosotros, sin dejar que voice.stop()
        # dispare el siguiente automáticamente
        queue.next()

        if voice.is_playing():
            self.player.ignore_after = True
            voice.stop()

        await self.player.play_current(ctx.guild)

        song = queue.current

        if song:
            await ctx.send(f"⏭️ Siguiente: **{song.title}**")

    @commands.command(name="b")
    async def previous_song(self, ctx):
        """Vuelve a la canción anterior."""

        voice = ctx.guild.voice_client

        if voice is None:
            await ctx.send("❌ No estoy en ningún canal de voz.")
            return

        queue = get_queue(ctx.guild.id)

        if not queue.has_previous():
            await ctx.send("⏮️ No hay una canción anterior.")
            return

        queue.previous()

        if voice.is_playing():
            self.player.ignore_after = True
            voice.stop()

        await self.player.play_current(ctx.guild)

        song = queue.current

        if song:
            await ctx.send(f"⏮️ Anterior: **{song.title}**")

    @commands.command(name="s")
    async def stop(self, ctx):
        """Detiene la reproducción sin avanzar la cola."""

        voice = ctx.guild.voice_client

        if voice is None or not voice.is_playing():
            await ctx.send("⏹️ No hay música reproduciéndose.")
            return

        self.player.ignore_after = True
        voice.stop()

        await ctx.send("⏹️ Música detenida.")

    @commands.command(name="leave")
    async def leave(self, ctx):
        """Hace que Foxy salga del canal de voz."""

        voice = ctx.guild.voice_client

        if voice is None:
            await ctx.send("❌ No estoy en un canal de voz.")
            return

        self.player.ignore_after = True

        await voice.disconnect()

        queue = get_queue(ctx.guild.id)
        queue.clear()

        await ctx.send("👋 He salido del canal de voz.")


async def setup_music(bot):
    await bot.add_cog(MusicCommands(bot))