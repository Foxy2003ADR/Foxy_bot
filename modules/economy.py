# modules/economy.py

"""
💰 Foxy Economy
Sistema de economía de Foxy.

Este módulo utiliza el dinero almacenado y gestionado
por modules/foxy_core.py.

No crea un segundo sistema de dinero.
"""

import random
import time

import discord
from discord.ext import commands

from modules.foxy_core import (
    obtener_foxy,
    añadir_dinero,
    quitar_dinero,
)


# ============================================================
# CONFIGURACIÓN
# ============================================================

DAILY_COOLDOWN = 24 * 60 * 60
TRABAJAR_COOLDOWN = 60

DAILY_MIN = 100
DAILY_MAX = 300

TRABAJAR_MIN = 25
TRABAJAR_MAX = 100


# ============================================================
# COOLDOWNS
# ============================================================

daily_cooldowns = {}
trabajar_cooldowns = {}


# ============================================================
# UTILIDADES
# ============================================================

def obtener_dinero():
    """
    Devuelve el dinero actual de Foxy.
    """

    foxy = obtener_foxy()

    return foxy.get("dinero", 0)


def formatear_dinero(cantidad):
    """
    Formatea una cantidad de dinero.
    """

    return f"{cantidad:,}".replace(",", ".")


def tiempo_restante(segundos):
    """
    Convierte segundos a un formato legible.
    """

    segundos = int(segundos)

    horas = segundos // 3600
    minutos = (segundos % 3600) // 60
    segundos = segundos % 60

    partes = []

    if horas > 0:
        partes.append(f"{horas}h")

    if minutos > 0:
        partes.append(f"{minutos}m")

    if segundos > 0 or not partes:
        partes.append(f"{segundos}s")

    return " ".join(partes)


# ============================================================
# COMANDO SALDO
# ============================================================

@commands.command(
    name="saldo",
    aliases=[
        "dinero",
        "balance",
        "wallet"
    ]
)
async def saldo(ctx):
    """
    Muestra el dinero actual de Foxy.
    """

    dinero = obtener_dinero()

    embed = discord.Embed(
        title="💰 Saldo de Foxy",
        description=(
            "🦊 **Foxy** tiene actualmente:\n\n"
            f"💰 **{formatear_dinero(dinero)} monedas**"
        ),
        color=discord.Color.gold()
    )

    await ctx.send(embed=embed)


# ============================================================
# COMANDO DAILY
# ============================================================

@commands.command(
    name="daily",
    aliases=[
        "diario",
        "recompensa"
    ]
)
async def daily(ctx):
    """
    Recompensa diaria de Foxy.
    """

    usuario_id = ctx.author.id
    ahora = time.time()

    ultimo_uso = daily_cooldowns.get(usuario_id)

    if ultimo_uso is not None:

        transcurrido = ahora - ultimo_uso

        if transcurrido < DAILY_COOLDOWN:

            restante = DAILY_COOLDOWN - transcurrido

            await ctx.send(
                "⏳ **Todavía no puedes reclamar el Daily.**\n"
                f"Vuelve en **{tiempo_restante(restante)}**."
            )

            return

    recompensa = random.randint(
        DAILY_MIN,
        DAILY_MAX
    )

    if not añadir_dinero(recompensa):

        await ctx.send(
            "❌ No se pudo añadir la recompensa."
        )

        return

    daily_cooldowns[usuario_id] = ahora

    dinero = obtener_dinero()

    embed = discord.Embed(
        title="🎁 Daily de Foxy",
        description=(
            "🦊 ¡Foxy ha recibido su recompensa diaria!\n\n"
            f"💰 Recompensa: "
            f"**+{formatear_dinero(recompensa)} monedas**\n"
            f"💳 Saldo: "
            f"**{formatear_dinero(dinero)} monedas**"
        ),
        color=discord.Color.green()
    )

    await ctx.send(embed=embed)


# ============================================================
# COMANDO TRABAJAR
# ============================================================

@commands.command(
    name="trabajar",
    aliases=[
        "work",
        "trabajo"
    ]
)
async def trabajar(ctx):
    """
    Foxy trabaja para conseguir dinero.
    """

    usuario_id = ctx.author.id
    ahora = time.time()

    ultimo_uso = trabajar_cooldowns.get(usuario_id)

    if ultimo_uso is not None:

        transcurrido = ahora - ultimo_uso

        if transcurrido < TRABAJAR_COOLDOWN:

            restante = TRABAJAR_COOLDOWN - transcurrido

            await ctx.send(
                "⏳ **Foxy está cansado.**\n"
                f"Puedes volver a trabajar en "
                f"**{tiempo_restante(restante)}**."
            )

            return

    trabajos = [
        "🛠️ Foxy ha trabajado en una tienda.",
        "📦 Foxy ha repartido paquetes.",
        "💻 Foxy ha hecho un trabajo de informática.",
        "🍕 Foxy ha trabajado en una pizzería.",
        "🚗 Foxy ha lavado coches.",
        "🎮 Foxy ha probado videojuegos.",
        "🐾 Foxy ha cuidado mascotas.",
        "🏪 Foxy ha ayudado en un supermercado.",
    ]

    trabajo = random.choice(trabajos)

    recompensa = random.randint(
        TRABAJAR_MIN,
        TRABAJAR_MAX
    )

    if not añadir_dinero(recompensa):

        await ctx.send(
            "❌ No se pudo añadir el dinero."
        )

        return

    trabajar_cooldowns[usuario_id] = ahora

    dinero = obtener_dinero()

    embed = discord.Embed(
        title="💼 Trabajo completado",
        description=(
            f"{trabajo}\n\n"
            f"💰 Has ganado: "
            f"**+{formatear_dinero(recompensa)} monedas**\n"
            f"💳 Saldo: "
            f"**{formatear_dinero(dinero)} monedas**"
        ),
        color=discord.Color.blue()
    )

    await ctx.send(embed=embed)


# ============================================================
# COMANDO PAGAR
# ============================================================

@commands.command(
    name="pagar",
    aliases=[
        "pay",
        "dar"
    ]
)
async def pagar(
    ctx,
    miembro: discord.Member = None,
    cantidad: int = None
):
    """
    Transfiere dinero de Foxy a otro usuario.

    Ejemplo:
    !pagar @Usuario 100
    """

    if miembro is None or cantidad is None:

        await ctx.send(
            "❌ Uso correcto:\n"
            "`!pagar @usuario cantidad`"
        )

        return

    if cantidad <= 0:

        await ctx.send(
            "❌ La cantidad debe ser mayor que **0**."
        )

        return

    if miembro.bot:

        await ctx.send(
            "❌ No puedes pagarle a un bot."
        )

        return

    if miembro.id == ctx.author.id:

        await ctx.send(
            "❌ No puedes pagarte a ti mismo."
        )

        return

    dinero = obtener_dinero()

    if dinero < cantidad:

        await ctx.send(
            "❌ Foxy no tiene suficiente dinero.\n"
            f"💰 Saldo: "
            f"**{formatear_dinero(dinero)} monedas**"
        )

        return

    if not quitar_dinero(cantidad):

        await ctx.send(
            "❌ No se pudo realizar el pago."
        )

        return

    embed = discord.Embed(
        title="💸 Pago realizado",
        description=(
            f"🦊 Foxy ha enviado dinero a "
            f"{miembro.mention}.\n\n"
            f"💰 Cantidad: "
            f"**{formatear_dinero(cantidad)} monedas**\n"
            f"💳 Saldo restante: "
            f"**{formatear_dinero(obtener_dinero())} monedas**"
        ),
        color=discord.Color.orange()
    )

    await ctx.send(embed=embed)


# ============================================================
# COMANDO ECONOMIA
# ============================================================

@commands.command(
    name="economia",
    aliases=[
        "eco",
        "economy"
    ]
)
async def economia(ctx):
    """
    Muestra el resumen económico de Foxy.
    """

    foxy = obtener_foxy()

    dinero = foxy.get(
        "dinero",
        0
    )

    embed = discord.Embed(
        title="💰 Economía de Foxy",
        color=discord.Color.gold()
    )

    embed.add_field(
        name="🦊 Jugador",
        value="Foxy",
        inline=True
    )

    embed.add_field(
        name="💰 Dinero",
        value=(
            f"**{formatear_dinero(dinero)}** monedas"
        ),
        inline=True
    )

    embed.add_field(
        name="⭐ Nivel",
        value=f"**{foxy.get('nivel', 1)}**",
        inline=True
    )

    embed.add_field(
        name="🎮 Partidas",
        value=f"**{foxy.get('partidas', 0)}**",
        inline=True
    )

    embed.add_field(
        name="🏆 Victorias",
        value=f"**{foxy.get('victorias', 0)}**",
        inline=True
    )

    embed.add_field(
        name="🔥 Racha",
        value=f"**{foxy.get('racha', 0)}**",
        inline=True
    )

    await ctx.send(embed=embed)


# ============================================================
# DAR DINERO
# ============================================================

@commands.command(
    name="dar_dinero"
)
@commands.has_permissions(
    administrator=True
)
async def dar_dinero(ctx, cantidad: int = None):
    """
    Añade dinero a Foxy.

    Solo administradores.

    Ejemplo:
    !dar_dinero 500
    """

    if cantidad is None:

        await ctx.send(
            "❌ Uso correcto:\n"
            "`!dar_dinero cantidad`"
        )

        return

    if cantidad <= 0:

        await ctx.send(
            "❌ La cantidad debe ser mayor que **0**."
        )

        return

    if not añadir_dinero(cantidad):

        await ctx.send(
            "❌ No se pudo añadir el dinero."
        )

        return

    await ctx.send(
        "💰 **Dinero añadido a Foxy.**\n"
        f"🦊 +**{formatear_dinero(cantidad)} monedas**\n"
        f"💳 Saldo actual: "
        f"**{formatear_dinero(obtener_dinero())} monedas**"
    )


# ============================================================
# QUITAR DINERO
# ============================================================

@commands.command(
    name="quitar_dinero"
)
@commands.has_permissions(
    administrator=True
)
async def quitar_dinero_comando(
    ctx,
    cantidad: int = None
):
    """
    Quita dinero de Foxy.

    Solo administradores.

    Ejemplo:
    !quitar_dinero 100
    """

    if cantidad is None:

        await ctx.send(
            "❌ Uso correcto:\n"
            "`!quitar_dinero cantidad`"
        )

        return

    if cantidad <= 0:

        await ctx.send(
            "❌ La cantidad debe ser mayor que **0**."
        )

        return

    if not quitar_dinero(cantidad):

        await ctx.send(
            "❌ Foxy no tiene suficiente dinero."
        )

        return

    await ctx.send(
        "💸 **Dinero retirado de Foxy.**\n"
        f"🦊 -**{formatear_dinero(cantidad)} monedas**\n"
        f"💳 Saldo actual: "
        f"**{formatear_dinero(obtener_dinero())} monedas**"
    )


# ============================================================
# ERRORES DE PERMISOS
# ============================================================

@dar_dinero.error
async def dar_dinero_error(ctx, error):

    if isinstance(
        error,
        commands.MissingPermissions
    ):

        await ctx.send(
            "❌ Solo los **administradores** pueden "
            "usar este comando."
        )


@quitar_dinero_comando.error
async def quitar_dinero_error(ctx, error):

    if isinstance(
        error,
        commands.MissingPermissions
    ):

        await ctx.send(
            "❌ Solo los **administradores** pueden "
            "usar este comando."
        )


# ============================================================
# SETUP
# ============================================================

def setup_economy(bot):
    """
    Carga el sistema de Economía.
    """

    bot.add_command(saldo)
    bot.add_command(daily)
    bot.add_command(trabajar)
    bot.add_command(pagar)
    bot.add_command(economia)
    bot.add_command(dar_dinero)
    bot.add_command(quitar_dinero_comando)

    print("💰 Sistema de Economía cargado")