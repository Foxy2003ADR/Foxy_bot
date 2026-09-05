import discord
from discord.ext import commands

from .config import (
    TWITCH_BROADCASTER_LOGIN,
    twitch_config_ok,
)
from .streams import get_stream, get_channel


def setup_twitch(bot):

    @bot.command(name="twitch")
    async def twitch(ctx):
        """
        Muestra el estado actual de la integración de Twitch.
        """

        embed = discord.Embed(
            title="🟣 Twitch de Foxy",
            color=discord.Color.purple()
        )

        # ----------------------------------------------------
        # CONFIGURACIÓN
        # ----------------------------------------------------

        if not twitch_config_ok():
            embed.description = (
                "⚠️ La integración de Twitch está creada, "
                "pero todavía falta configurar las credenciales."
            )

            embed.add_field(
                name="📡 Estado",
                value="⚠️ Configuración incompleta",
                inline=False
            )

            await ctx.send(embed=embed)
            return

        # ----------------------------------------------------
        # INFORMACIÓN DEL CANAL
        # ----------------------------------------------------

        try:
            channel = await get_channel(
                TWITCH_BROADCASTER_LOGIN
            )

            stream = await get_stream(
                TWITCH_BROADCASTER_LOGIN
            )

        except Exception as error:
            embed.description = (
                "❌ No se pudo conectar con la API de Twitch."
            )

            embed.add_field(
                name="Error",
                value=f"`{error}`",
                inline=False
            )

            await ctx.send(embed=embed)
            return

        # ----------------------------------------------------
        # CANAL NO ENCONTRADO
        # ----------------------------------------------------

        if channel is None:
            embed.description = (
                "❌ No se encontró el canal de Twitch."
            )

            await ctx.send(embed=embed)
            return

        # ----------------------------------------------------
        # ESTADO DEL DIRECTO
        # ----------------------------------------------------

        if stream is None:

            embed.description = (
                f"📺 Canal: **{TWITCH_BROADCASTER_LOGIN}**"
            )

            embed.add_field(
                name="📡 Estado",
                value="⚫ Offline",
                inline=False
            )

        else:

            embed.description = (
                f"📺 Canal: **{TWITCH_BROADCASTER_LOGIN}**"
            )

            embed.add_field(
                name="📡 Estado",
                value="🔴 EN DIRECTO",
                inline=False
            )

            embed.add_field(
                name="🎮 Categoría",
                value=stream.get(
                    "game_name",
                    "Desconocida"
                ),
                inline=True
            )

            embed.add_field(
                name="👀 Espectadores",
                value=str(
                    stream.get(
                        "viewer_count",
                        0
                    )
                ),
                inline=True
            )

            embed.add_field(
                name="📝 Título",
                value=stream.get(
                    "title",
                    "Sin título"
                ),
                inline=False
            )

            thumbnail = stream.get("thumbnail_url")

            if thumbnail:
                thumbnail = thumbnail.replace(
                    "{width}",
                    "1280"
                ).replace(
                    "{height}",
                    "720"
                )

                embed.set_image(
                    url=thumbnail
                )

        # ----------------------------------------------------
        # INFORMACIÓN DEL CANAL
        # ----------------------------------------------------

        embed.add_field(
            name="👤 Canal",
            value=channel.get(
                "display_name",
                TWITCH_BROADCASTER_LOGIN
            ),
            inline=True
        )

        embed.add_field(
            name="🎮 Categoría actual",
            value=channel.get(
                "game_name",
                "Ninguna"
            ),
            inline=True
        )

        embed.set_footer(
            text="🟣 DC_Foxy_Bot • Twitch"
        )

        await ctx.send(embed=embed)