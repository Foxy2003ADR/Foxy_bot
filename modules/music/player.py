import asyncio

import discord

from .queue import get_queue
from .sources import get_audio_url


FFMPEG_OPTIONS = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-vn",
}


class MusicPlayer:
    def __init__(self, bot):
        self.bot = bot
        self.ignore_after = False

    async def play_current(self, guild: discord.Guild):
        """Reproduce la canción que está actualmente seleccionada."""

        voice = guild.voice_client

        if voice is None or not voice.is_connected():
            return

        queue = get_queue(guild.id)
        song = queue.current

        if song is None:
            return

        try:
            audio_url = await get_audio_url(song.webpage_url)

            source = discord.FFmpegPCMAudio(
                audio_url,
                **FFMPEG_OPTIONS
            )

            def after_playing(error):
                if error:
                    print(f"[Music] Error reproduciendo: {error}")

                # Si fue !n, !b, !s o !leave, no avanzar automáticamente
                if self.ignore_after:
                    self.ignore_after = False
                    return

                asyncio.run_coroutine_threadsafe(
                    self.play_next(guild),
                    self.bot.loop
                )

            voice.play(source, after=after_playing)

            print(f"[Music] ▶️ Reproduciendo: {song.title}")

        except Exception as error:
            print(
                f"[Music] No se pudo reproducir "
                f"'{song.title}': {error}"
            )

            # Intentar automáticamente con la siguiente canción
            await self.play_next(guild)

    async def play_next(self, guild: discord.Guild):
        """Avanza a la siguiente canción y la reproduce."""

        queue = get_queue(guild.id)

        if not queue.has_next():
            return

        queue.next()

        await self.play_current(guild)

    async def stop(self, guild: discord.Guild):
        """Detiene la reproducción sin avanzar la cola."""

        voice = guild.voice_client

        if voice and voice.is_playing():
            self.ignore_after = True
            voice.stop()

    async def disconnect(self, guild: discord.Guild):
        """Desconecta al bot del canal de voz."""

        voice = guild.voice_client

        if voice and voice.is_connected():
            self.ignore_after = True
            await voice.disconnect()