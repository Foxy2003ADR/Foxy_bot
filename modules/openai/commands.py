import discord
from discord.ext import commands

from .client import ask_openai
from .config import openai_config_ok


def setup_openai(bot):

    @bot.command(name="ia")
    async def ia(ctx, *, pregunta: str = None):

        if not openai_config_ok():
            await ctx.send(
                "❌ OpenAI no está configurado todavía."
            )
            return

        if not pregunta:
            await ctx.send(
                "🤖 Escribe algo después de `!ia`."
            )
            return

        try:
            respuesta = await ask_openai(
                pregunta
            )

            if len(respuesta) > 2000:
                respuesta = respuesta[:1997] + "..."

            await ctx.send(
                respuesta
            )

        except Exception as error:
            await ctx.send(
                "❌ Ha ocurrido un error con OpenAI."
            )

            print(
                f"[OpenAI] Error: {error}"
            )