import asyncio
import os
import discord

from .speech import (
    generar_voz_animatronica,
    borrar_archivo
)


# ============================================================
# 🎙️ TTS — ESTADO
# ============================================================

# Evita que varios mensajes se reproduzcan
# simultáneamente en el mismo servidor.
reproduciendo = {}


# ============================================================
# 🎙️ REPRODUCIR AUDIO
# ============================================================

async def reproducir_tts(
    message: discord.Message,
    texto: str
):
    guild = message.guild

    if guild is None:
        return

    autor = message.author

    # --------------------------------------------------------
    # Comprobar que el usuario está conectado a voz
    # --------------------------------------------------------

    if not isinstance(
        autor,
        discord.Member
    ):
        return

    canal_voz = autor.voice.channel if autor.voice else None

    if canal_voz is None:
        return

    # --------------------------------------------------------
    # Evitar mensajes simultáneos
    # --------------------------------------------------------

    if reproduciendo.get(
        guild.id,
        False
    ):
        return

    reproduciendo[guild.id] = True

    original = None
    procesado = None

    try:

        # ----------------------------------------------------
        # Obtener conexión actual de Foxy
        # ----------------------------------------------------

        voice_client = guild.voice_client

        # ----------------------------------------------------
        # Si Foxy no está conectado, entrar
        # ----------------------------------------------------

        if voice_client is None:

            voice_client = await canal_voz.connect(
                self_deaf=True
            )

        # ----------------------------------------------------
        # Si Foxy está en otro canal, moverse al del usuario
        # ----------------------------------------------------

        elif voice_client.channel.id != canal_voz.id:

            await voice_client.move_to(
                canal_voz
            )

        # ----------------------------------------------------
        # Generar voz + efecto animatrónico
        # ----------------------------------------------------

        original, procesado = (
            await generar_voz_animatronica(
                texto
            )
        )

        # ----------------------------------------------------
        # Crear fuente de audio
        # ----------------------------------------------------

        fuente = discord.FFmpegPCMAudio(
            procesado
        )

        # ----------------------------------------------------
        # Esperar a que termine la reproducción
        # ----------------------------------------------------

        terminado = asyncio.Event()

        loop = asyncio.get_running_loop()

        def cuando_termine(error):
            if error:
                print(
                    f"❌ Error reproduciendo TTS: {error}"
                )

            loop.call_soon_threadsafe(
                terminado.set
            )

        voice_client.play(
            fuente,
            after=cuando_termine
        )

        await terminado.wait()

    except Exception as error:

        print(
            f"❌ Error en TTS: {error}"
        )

    finally:

        # ----------------------------------------------------
        # Liberar archivos temporales
        # ----------------------------------------------------

        borrar_archivo(
            original
        )

        borrar_archivo(
            procesado
        )

        reproduciendo[
            guild.id
        ] = False


# ============================================================
# 🎙️ LISTENER DE MENSAJES
# ============================================================

async def procesar_mensaje_tts(
    message: discord.Message
):

    # --------------------------------------------------------
    # Ignorar bots
    # --------------------------------------------------------

    if message.author.bot:
        return

    # --------------------------------------------------------
    # Ignorar mensajes privados
    # --------------------------------------------------------

    if message.guild is None:
        return

    # --------------------------------------------------------
    # Ignorar comandos
    # --------------------------------------------------------

    if message.content.startswith("!"):
        return

    # --------------------------------------------------------
    # Ignorar mensajes vacíos
    # --------------------------------------------------------

    texto = message.content.strip()

    if not texto:
        return

    # --------------------------------------------------------
    # Comprobar si el usuario está en voz
    # --------------------------------------------------------

    if not isinstance(
        message.author,
        discord.Member
    ):
        return

    if message.author.voice is None:
        return

    if message.author.voice.channel is None:
        return

    # --------------------------------------------------------
    # Limitar mensajes excesivamente largos
    # --------------------------------------------------------

    texto = texto[:500]

    # --------------------------------------------------------
    # Reproducir
    # --------------------------------------------------------

    await reproducir_tts(
        message,
        texto
    )


# ============================================================
# 🎙️ SETUP DEL MÓDULO
# ============================================================

def setup_tts(bot):

    @bot.listen("on_message")
    async def tts_on_message(
        message: discord.Message
    ):
        await procesar_mensaje_tts(
            message
        )