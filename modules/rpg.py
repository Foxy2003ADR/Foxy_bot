# modules/rpg.py

"""
🦊 Foxy RPG
Sistema RPG de Foxy.

Utiliza directamente modules/foxy_core.py
para XP, nivel, vida, energía y estado.
"""

import random

import discord
from discord.ext import commands

from modules.foxy_core import (
    obtener_foxy,
    añadir_xp,
    curar,
    recibir_daño,
    gastar_energia,
    recuperar_energia,
    cambiar_estado,
    obtener_estadisticas,
    resumen_foxy,
)


# ============================================================
# CONFIGURACIÓN
# ============================================================

XP_ENTRENAR_MIN = 15
XP_ENTRENAR_MAX = 35

ENERGIA_ENTRENAR = 20

ENERGIA_DESCANSAR = 10

CURACION_DESCANSAR = 15


# ============================================================
# UTILIDADES
# ============================================================

def porcentaje(valor, maximo):
    """
    Calcula un porcentaje de forma segura.
    """

    if maximo <= 0:
        return 0

    return int((valor / maximo) * 100)


def barra(valor, maximo, bloques=10):
    """
    Crea una barra visual.
    """

    if maximo <= 0:
        return "░" * bloques

    llenos = int((valor / maximo) * bloques)

    llenos = max(
        0,
        min(llenos, bloques)
    )

    return (
        "█" * llenos
        + "░" * (bloques - llenos)
    )


# ============================================================
# COMANDO FOXY
# ============================================================

@commands.command(
    name="foxy",
    aliases=[
        "perfil",
        "profile"
    ]
)
async def foxy(ctx):
    """
    Muestra el perfil completo de Foxy.
    """

    datos = obtener_foxy()

    nivel = datos.get("nivel", 1)
    xp = datos.get("xp", 0)

    vida = datos.get("vida", 100)
    vida_maxima = datos.get("vida_maxima", 100)

    energia = datos.get("energia", 100)
    energia_maxima = datos.get("energia_maxima", 100)

    estado = datos.get(
        "estado",
        "Feliz"
    )

    dinero = datos.get(
        "dinero",
        0
    )

    embed = discord.Embed(
        title="🦊 Perfil de Foxy",
        color=discord.Color.orange()
    )

    embed.add_field(
        name="⭐ Nivel",
        value=f"**{nivel}**",
        inline=True
    )

    embed.add_field(
        name="✨ XP",
        value=f"**{xp}**",
        inline=True
    )

    embed.add_field(
        name="💰 Dinero",
        value=f"**{dinero}**",
        inline=True
    )

    embed.add_field(
        name="❤️ Vida",
        value=(
            f"**{vida}/{vida_maxima}**\n"
            f"{barra(vida, vida_maxima)}"
        ),
        inline=True
    )

    embed.add_field(
        name="⚡ Energía",
        value=(
            f"**{energia}/{energia_maxima}**\n"
            f"{barra(energia, energia_maxima)}"
        ),
        inline=True
    )

    embed.add_field(
        name="🎭 Estado",
        value=f"**{estado}**",
        inline=True
    )

    embed.add_field(
        name="🎮 Partidas",
        value=f"**{datos.get('partidas', 0)}**",
        inline=True
    )

    embed.add_field(
        name="🏆 Victorias",
        value=f"**{datos.get('victorias', 0)}**",
        inline=True
    )

    embed.add_field(
        name="🔥 Racha",
        value=f"**{datos.get('racha', 0)}**",
        inline=True
    )

    await ctx.send(embed=embed)


# ============================================================
# COMANDO XP
# ============================================================

@commands.command(
    name="xp",
    aliases=[
        "experiencia",
        "nivel"
    ]
)
async def xp(ctx):
    """
    Muestra el nivel y XP de Foxy.
    """

    datos = obtener_foxy()

    nivel = datos.get(
        "nivel",
        1
    )

    experiencia = datos.get(
        "xp",
        0
    )

    xp_necesaria = nivel * 100

    progreso = porcentaje(
        experiencia,
        xp_necesaria
    )

    embed = discord.Embed(
        title="✨ Experiencia de Foxy",
        description=(
            f"⭐ Nivel actual: **{nivel}**\n\n"
            f"✨ XP: **{experiencia}/{xp_necesaria}**\n"
            f"{barra(experiencia, xp_necesaria)}\n\n"
            f"📊 Progreso: **{progreso}%**"
        ),
        color=discord.Color.purple()
    )

    await ctx.send(embed=embed)


# ============================================================
# COMANDO ENTRENAR
# ============================================================

@commands.command(
    name="entrenar",
    aliases=[
        "train"
    ]
)
async def entrenar(ctx):
    """
    Entrena a Foxy y obtiene XP.
    """

    datos_antes = obtener_foxy()

    energia = datos_antes.get(
        "energia",
        100
    )

    if energia < ENERGIA_ENTRENAR:

        await ctx.send(
            "❌ **Foxy está demasiado cansado.**\n"
            f"⚡ Necesita al menos **{ENERGIA_ENTRENAR} energía**."
        )

        return

    gastar_energia(
        ENERGIA_ENTRENAR
    )

    experiencia = random.randint(
        XP_ENTRENAR_MIN,
        XP_ENTRENAR_MAX
    )

    nivel_antes = datos_antes.get(
        "nivel",
        1
    )

    subio_nivel = añadir_xp(
        experiencia
    )

    datos = obtener_foxy()

    nivel_despues = datos.get(
        "nivel",
        1
    )

    mensaje_nivel = ""

    if subio_nivel or nivel_despues > nivel_antes:

        mensaje_nivel = (
            "\n\n"
            "🎉 **¡FOXY HA SUBIDO DE NIVEL!**\n"
            f"⭐ Ahora es nivel **{nivel_despues}**."
        )

    await ctx.send(
        "🥊 **Foxy ha entrenado.**\n\n"
        f"✨ XP conseguida: **+{experiencia}**\n"
        f"⚡ Energía gastada: **-{ENERGIA_ENTRENAR}**"
        f"{mensaje_nivel}"
    )


# ============================================================
# COMANDO DESCANSAR
# ============================================================

@commands.command(
    name="descansar",
    aliases=[
        "rest",
        "dormir"
    ]
)
async def descansar(ctx):
    """
    Foxy descansa y recupera energía y vida.
    """

    datos = obtener_foxy()

    energia = datos.get(
        "energia",
        100
    )

    energia_maxima = datos.get(
        "energia_maxima",
        100
    )

    vida = datos.get(
        "vida",
        100
    )

    vida_maxima = datos.get(
        "vida_maxima",
        100
    )

    if (
        energia >= energia_maxima
        and vida >= vida_maxima
    ):

        await ctx.send(
            "😴 Foxy ya está completamente descansado."
        )

        return

    recuperar_energia(
        ENERGIA_DESCANSAR
    )

    curar(
        CURACION_DESCANSAR
    )

    cambiar_estado(
        "Descansado"
    )

    datos = obtener_foxy()

    energia = datos.get(
        "energia",
        100
    )

    vida = datos.get(
        "vida",
        100
    )

    await ctx.send(
        "😴 **Foxy ha descansado.**\n\n"
        f"❤️ Vida: **{vida}/{vida_maxima}**\n"
        f"⚡ Energía: **{energia}/{energia_maxima}**\n"
        "🎭 Estado: **Descansado**"
    )


# ============================================================
# COMANDO CURAR
# ============================================================

@commands.command(
    name="curar",
    aliases=[
        "heal"
    ]
)
async def curar_comando(ctx, cantidad: int = 25):
    """
    Cura a Foxy.

    Ejemplo:
    !curar
    !curar 50
    """

    if cantidad <= 0:

        await ctx.send(
            "❌ La cantidad debe ser mayor que **0**."
        )

        return

    datos = obtener_foxy()

    vida_antes = datos.get(
        "vida",
        100
    )

    vida_maxima = datos.get(
        "vida_maxima",
        100
    )

    if vida_antes >= vida_maxima:

        await ctx.send(
            "❤️ Foxy ya tiene la vida al máximo."
        )

        return

    curar(
        cantidad
    )

    datos = obtener_foxy()

    vida_despues = datos.get(
        "vida",
        100
    )

    recuperada = vida_despues - vida_antes

    cambiar_estado(
        "Recuperado"
    )

    await ctx.send(
        "❤️ **Foxy se ha curado.**\n\n"
        f"❤️ Vida recuperada: **+{recuperada}**\n"
        f"❤️ Vida actual: **{vida_despues}/{vida_maxima}**"
    )


# ============================================================
# COMANDO ESTADO
# ============================================================

@commands.command(
    name="estado",
    aliases=[
        "status"
    ]
)
async def estado(ctx):
    """
    Muestra el estado actual de Foxy.
    """

    datos = obtener_foxy()

    vida = datos.get(
        "vida",
        100
    )

    vida_maxima = datos.get(
        "vida_maxima",
        100
    )

    energia = datos.get(
        "energia",
        100
    )

    energia_maxima = datos.get(
        "energia_maxima",
        100
    )

    estado_actual = datos.get(
        "estado",
        "Feliz"
    )

    embed = discord.Embed(
        title="🦊 Estado de Foxy",
        color=discord.Color.green()
    )

    embed.add_field(
        name="❤️ Vida",
        value=(
            f"**{vida}/{vida_maxima}**\n"
            f"{barra(vida, vida_maxima)}"
        ),
        inline=False
    )

    embed.add_field(
        name="⚡ Energía",
        value=(
            f"**{energia}/{energia_maxima}**\n"
            f"{barra(energia, energia_maxima)}"
        ),
        inline=False
    )

    embed.add_field(
        name="🎭 Estado",
        value=f"**{estado_actual}**",
        inline=False
    )

    await ctx.send(embed=embed)


# ============================================================
# COMANDO STATS
# ============================================================

@commands.command(
    name="stats",
    aliases=[
        "estadisticas",
        "estadísticas"
    ]
)
async def stats(ctx):
    """
    Muestra las estadísticas de Foxy.
    """

    datos = obtener_estadisticas()

    embed = discord.Embed(
        title="📊 Estadísticas de Foxy",
        color=discord.Color.blue()
    )

    embed.add_field(
        name="🎮 Partidas",
        value=f"**{datos['partidas']}**",
        inline=True
    )

    embed.add_field(
        name="🏆 Victorias",
        value=f"**{datos['victorias']}**",
        inline=True
    )

    embed.add_field(
        name="❌ Derrotas",
        value=f"**{datos['derrotas']}**",
        inline=True
    )

    embed.add_field(
        name="🔥 Racha actual",
        value=f"**{datos['racha']}**",
        inline=True
    )

    embed.add_field(
        name="👑 Mejor racha",
        value=f"**{datos['mejor_racha']}**",
        inline=True
    )

    if datos["partidas"] > 0:

        porcentaje_victorias = (
            datos["victorias"]
            / datos["partidas"]
        ) * 100

    else:

        porcentaje_victorias = 0

    embed.add_field(
        name="📈 Winrate",
        value=f"**{porcentaje_victorias:.1f}%**",
        inline=True
    )

    await ctx.send(embed=embed)


# ============================================================
# COMANDO RESUMEN
# ============================================================

@commands.command(
    name="resumen_foxy",
    aliases=[
        "resumen"
    ]
)
async def resumen(ctx):
    """
    Muestra un resumen rápido de Foxy.
    """

    await ctx.send(
        resumen_foxy()
    )


# ============================================================
# COMANDO DAÑO
# ============================================================

@commands.command(
    name="dañar_foxy",
    aliases=[
        "danar_foxy"
    ]
)
@commands.has_permissions(
    administrator=True
)
async def danar_foxy(ctx, cantidad: int = 10):
    """
    Hace daño a Foxy.

    Solo administradores.

    Ejemplo:
    !dañar_foxy 20
    """

    if cantidad <= 0:

        await ctx.send(
            "❌ La cantidad debe ser mayor que **0**."
        )

        return

    recibir_daño(
        cantidad
    )

    datos = obtener_foxy()

    await ctx.send(
        "⚔️ **Foxy ha recibido daño.**\n\n"
        f"❤️ Vida actual: "
        f"**{datos['vida']}/{datos['vida_maxima']}**"
    )


# ============================================================
# ERRORES
# ============================================================

@danar_foxy.error
async def danar_foxy_error(ctx, error):

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

def setup_rpg(bot):
    """
    Carga el sistema RPG.
    """

    bot.add_command(foxy)
    bot.add_command(xp)
    bot.add_command(entrenar)
    bot.add_command(descansar)
    bot.add_command(curar_comando)
    bot.add_command(estado)
    bot.add_command(stats)
    bot.add_command(resumen)
    bot.add_command(danar_foxy)

    print("🎮 Sistema RPG cargado")