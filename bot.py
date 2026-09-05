# ============================================================
# 🦊 DC_FOXY_BOT — BOT PRINCIPAL
# ============================================================
#
# Versión:
# - Un solo bot.py
# - Carga segura de módulos
# - Protección contra comandos duplicados
# - Protección contra aliases duplicados
# - Comandos legacy compatibles
# - RPG
# - Economía
# - Inventario
# - Tienda
# - Juegos
# - Game Client
# - Música
# - TTS
# - 🔊 Voice Auto
# - 🟣 Twitch
# - 🤖 OpenAI
# - Seguridad
# - Logs
# - Foxy AI
# - XP legacy
# - Ayuda avanzada
# - Estado
# - Diagnóstico
# - Cierre limpio
# - ⛔ Discord opcional
#
# ============================================================


# ============================================================
# 1. IMPORTACIONES
# ============================================================

import os
import asyncio
import inspect
import random
import logging
import time
import traceback

from typing import Optional, Callable

import discord
from discord.ext import commands
from dotenv import load_dotenv


# ============================================================
# 2. CARGAR .ENV
# ============================================================

load_dotenv()


# ============================================================
# 3. IMPORTAR MÓDULOS
# ============================================================

# 🎮 Juegos
from modules.games import setup_games

# 🛡️ Seguridad
from modules.security import setup_security

# 📋 Logs
from modules.logs import setup_logs

# 🤖 IA de Foxy
from modules.foxy_ai import setup_foxy_ai

# 🤖 OpenAI
from modules.openai import setup_openai

# 🦊 Foxy Core
from modules.foxy_core import setup_foxy_core

# 🦊 Foxy Player
from modules.foxy_player import (
    crear_foxy,
    es_foxy,
    nombre_jugador,
    mencion_jugador,
    foxy_puede_unirse
)

# ⭐ RPG
from modules.rpg import setup_rpg

# 💰 Economía
from modules.economy import setup_economy

# 🎒 Inventario
from modules.inventory import setup_inventory

# 🛒 Tienda
from modules.shop import setup_shop

# 🎮 Game Client
from modules.game_client import setup_game_client

# 🎵 Música
from modules.music import setup_music

# 🎙️ TTS
from modules.tts import setup_tts

# 🔊 Voice Auto
from modules.voice_auto import setup_voice_auto

# 🟣 Twitch
from modules.twitch import setup_twitch


# ============================================================
# 4. CONFIGURACIÓN GENERAL
# ============================================================

PREFIX = "!"

BOT_NAME = "DC_Foxy_Bot"

BOT_VERSION = "3.2"

BOT_DESCRIPTION = (
    "Foxy Bot — RPG, economía, juegos, IA, "
    "moderación, Game Client, música, TTS, "
    "voz automática, Twitch y OpenAI"
)

STARTING_COINS = 100

XP_MIN = 15
XP_MAX = 25

LEVEL_XP_BASE = 100


# ============================================================
# 5. LOGGING
# ============================================================

LOG_LEVEL = os.getenv(
    "FOXY_LOG_LEVEL",
    "INFO"
).upper()

logging.basicConfig(
    level=getattr(
        logging,
        LOG_LEVEL,
        logging.INFO
    ),
    format=(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(name)s | "
        "%(message)s"
    )
)

logger = logging.getLogger(
    "DC_FOXY_BOT"
)


# ============================================================
# 6. INTENTS
# ============================================================

intents = discord.Intents.default()

intents.message_content = True
intents.members = True
intents.guilds = True
intents.messages = True
intents.reactions = True
intents.voice_states = True


# ============================================================
# 7. CREAR BOT
# ============================================================

bot = commands.Bot(
    command_prefix=PREFIX,
    intents=intents,
    help_command=None,
    case_insensitive=True
)


# ============================================================
# 8. DATOS LOCALES LEGACY
# ============================================================

economia = {}

niveles = {}

cooldowns_legacy = {}


estadisticas_bot = {
    "inicio": time.time(),
    "mensajes": 0,
    "comandos": 0,
    "errores": 0,
    "xp_otorgado": 0,
    "usuarios_creados": 0,
}


# ============================================================
# 9. CONTROL DE SISTEMAS
# ============================================================

sistemas_cargados = {}

bot_listo = False

modulos_cargando = False

inicializaciones_realizadas = set()


# ============================================================
# 10. UTILIDADES
# ============================================================

def obtener_economia_legacy(
    user_id: int
):
    """
    Obtiene el registro económico legacy.
    """

    if user_id not in economia:

        economia[user_id] = {
            "monedas": STARTING_COINS
        }

        estadisticas_bot[
            "usuarios_creados"
        ] += 1

    return economia[user_id]


# ============================================================

def obtener_nivel_legacy(
    user_id: int
):
    """
    Obtiene el registro de XP legacy.
    """

    if user_id not in niveles:

        niveles[user_id] = {
            "xp": 0,
            "nivel": 1
        }

    return niveles[user_id]


# ============================================================

def nivel_necesario(
    nivel: int
):
    """
    XP necesaria para subir al siguiente nivel.
    """

    if nivel <= 1:
        return LEVEL_XP_BASE

    return nivel * LEVEL_XP_BASE


# ============================================================

def texto_barra(
    actual: int,
    maximo: int,
    longitud: int = 10
):
    """
    Crea una barra visual de progreso.
    """

    if maximo <= 0:
        maximo = 1

    porcentaje = max(
        0,
        min(
            1,
            actual / maximo
        )
    )

    llenos = int(
        porcentaje * longitud
    )

    vacios = (
        longitud - llenos
    )

    return (
        "🟩" * llenos +
        "⬜" * vacios
    )


# ============================================================

def tiempo_humano(
    segundos: float
):
    """
    Convierte segundos en texto legible.
    """

    segundos = max(
        0,
        int(segundos)
    )

    dias, resto = divmod(
        segundos,
        86400
    )

    horas, resto = divmod(
        resto,
        3600
    )

    minutos, segundos = divmod(
        resto,
        60
    )

    partes = []

    if dias:
        partes.append(
            f"{dias}d"
        )

    if horas:
        partes.append(
            f"{horas}h"
        )

    if minutos:
        partes.append(
            f"{minutos}m"
        )

    if segundos or not partes:
        partes.append(
            f"{segundos}s"
        )

    return " ".join(
        partes
    )


# ============================================================

def es_administrador(
    member: discord.Member
):
    """
    Comprueba si un miembro es administrador.
    """

    if not member:
        return False

    return member.guild_permissions.administrator


# ============================================================

async def enviar_seguro(
    ctx,
    contenido: str = None,
    *,
    embed=None,
    ephemeral: bool = False
):
    """
    Envía un mensaje evitando errores comunes.
    """

    try:

        kwargs = {}

        if contenido is not None:
            kwargs["content"] = contenido

        if embed is not None:
            kwargs["embed"] = embed

        # Los comandos prefix no soportan ephemeral
        # mediante ctx.send().
        # Se conserva el parámetro por compatibilidad.
        _ = ephemeral

        return await ctx.send(
            **kwargs
        )

    except discord.Forbidden:

        logger.warning(
            "No se pudo enviar mensaje en #%s",
            getattr(
                getattr(
                    ctx,
                    "channel",
                    None
                ),
                "name",
                "desconocido"
            )
        )

    except discord.HTTPException as error:

        logger.error(
            "Discord HTTPException al enviar mensaje: %s",
            error
        )

    return None


# ============================================================
# 11. NORMALIZACIÓN DE NOMBRES DE COMANDOS
# ============================================================

def normalizar_nombre_comando(
    nombre: str
):
    """
    Normaliza nombres y aliases.
    """

    if not nombre:
        return ""

    return str(
        nombre
    ).strip().lower()


# ============================================================

def nombres_de_comando(
    command
):
    """
    Devuelve nombre principal y aliases.
    """

    nombres = []

    principal = getattr(
        command,
        "name",
        None
    )

    if principal:

        nombres.append(
            normalizar_nombre_comando(
                principal
            )
        )

    aliases = getattr(
        command,
        "aliases",
        []
    ) or []

    for alias in aliases:

        alias_normalizado = (
            normalizar_nombre_comando(
                alias
            )
        )

        if alias_normalizado:

            nombres.append(
                alias_normalizado
            )

    return list(
        dict.fromkeys(
            nombres
        )
    )


# ============================================================
# 12. DECORADOR DE COMANDOS LEGACY
# ============================================================

def legacy_command(
    name: Optional[str] = None,
    aliases=None,
    **kwargs
):
    """
    Registra un comando antiguo evitando conflictos.
    """

    aliases = aliases or []

    def decorator(func):

        command_name = (
            name
            if name
            else func.__name__
        )

        command_name_normalizado = (
            normalizar_nombre_comando(
                command_name
            )
        )

        aliases_normalizados = [
            normalizar_nombre_comando(
                alias
            )
            for alias in aliases
            if alias
        ]

        nombres_a_comprobar = [
            command_name_normalizado,
            *aliases_normalizados
        ]

        for nombre_comando in (
            nombres_a_comprobar
        ):

            if not nombre_comando:
                continue

            existente = bot.get_command(
                nombre_comando
            )

            if existente is not None:

                logger.warning(
                    "⏭️ Comando legacy omitido: !%s "
                    "(ya existe: !%s)",
                    command_name,
                    getattr(
                        existente,
                        "name",
                        "desconocido"
                    )
                )

                return func

        comando = commands.Command(
            func,
            name=command_name,
            aliases=aliases,
            **kwargs
        )

        for nombre_comando in (
            nombres_de_comando(
                comando
            )
        ):

            if bot.get_command(
                nombre_comando
            ) is not None:

                logger.warning(
                    "⏭️ Legacy !%s cancelado: "
                    "conflicto detectado con !%s",
                    command_name,
                    nombre_comando
                )

                return func

        try:

            bot.add_command(
                comando
            )

            logger.info(
                "✅ Comando legacy registrado: !%s",
                command_name
            )

        except commands.CommandRegistrationError as error:

            logger.warning(
                "⏭️ No se pudo registrar !%s: %s",
                command_name,
                error
            )

        return func

    return decorator


# ============================================================
# 13. CARGADOR SEGURO DE MÓDULOS
# ============================================================

def cargar_modulo_seguro(
    nombre: str,
    funcion: Callable
):
    """
    Carga un módulo evitando comandos duplicados.
    """

    global modulos_cargando

    if sistemas_cargados.get(
        nombre
    ):

        logger.warning(
            "⚠️ El módulo %s ya estaba cargado.",
            nombre
        )

        return True

    logger.info(
        "🔄 Cargando módulo: %s",
        nombre
    )

    add_command_original = (
        bot.add_command
    )

    def add_command_seguro(
        command,
        *args,
        **kwargs
    ):

        if command is None:
            return None

        nombres = nombres_de_comando(
            command
        )

        for nombre_comando in nombres:

            existente = bot.get_command(
                nombre_comando
            )

            if existente is not None:

                logger.warning(
                    "⚠️ [%s] Comando duplicado "
                    "detectado: !%s. "
                    "Se conserva el existente !%s.",
                    nombre,
                    nombre_comando,
                    getattr(
                        existente,
                        "name",
                        "desconocido"
                    )
                )

                return None

        try:

            return add_command_original(
                command,
                *args,
                **kwargs
            )

        except commands.CommandRegistrationError as error:

            logger.warning(
                "⚠️ [%s] Comando rechazado: %s",
                nombre,
                error
            )

            return None

    try:

        bot.add_command = (
            add_command_seguro
        )

        modulos_cargando = True

        resultado = funcion(
            bot
        )

        if inspect.isawaitable(
            resultado
        ):

            try:

                asyncio.run(
                    resultado
                )

            except RuntimeError as error:

                logger.warning(
                    "⚠️ [%s] No se pudo ejecutar "
                    "la inicialización async: %s",
                    nombre,
                    error
                )

        sistemas_cargados[
            nombre
        ] = True

        logger.info(
            "✅ Módulo cargado correctamente: %s",
            nombre
        )

        return True

    except Exception as error:

        sistemas_cargados[
            nombre
        ] = False

        estadisticas_bot[
            "errores"
        ] += 1

        logger.error(
            "❌ Error cargando módulo %s: %s",
            nombre,
            error
        )

        traceback.print_exc()

        return False

    finally:

        modulos_cargando = False

        bot.add_command = (
            add_command_original
        )


# ============================================================
# 14. CARGAR SISTEMAS
# ============================================================

logger.info(
    "=================================================="
)

logger.info(
    "🦊 INICIANDO DC_FOXY_BOT"
)

logger.info(
    "=================================================="
)


cargar_modulo_seguro(
    "Foxy Core",
    setup_foxy_core
)

cargar_modulo_seguro(
    "Security",
    setup_security
)

cargar_modulo_seguro(
    "Logs",
    setup_logs
)

cargar_modulo_seguro(
    "Games",
    setup_games
)

cargar_modulo_seguro(
    "Game Client",
    setup_game_client
)

cargar_modulo_seguro(
    "Music",
    setup_music
)

cargar_modulo_seguro(
    "TTS",
    setup_tts
)

cargar_modulo_seguro(
    "Voice Auto",
    setup_voice_auto
)

cargar_modulo_seguro(
    "Twitch",
    setup_twitch
)

cargar_modulo_seguro(
    "OpenAI",
    setup_openai
)

cargar_modulo_seguro(
    "RPG",
    setup_rpg
)

cargar_modulo_seguro(
    "Economy",
    setup_economy
)

cargar_modulo_seguro(
    "Inventory",
    setup_inventory
)

cargar_modulo_seguro(
    "Shop",
    setup_shop
)

cargar_modulo_seguro(
    "Foxy AI",
    setup_foxy_ai
)


# ============================================================
# 15. COMPROBAR COMANDOS REGISTRADOS
# ============================================================

logger.info(
    "=================================================="
)

logger.info(
    "📋 COMANDOS REGISTRADOS"
)

logger.info(
    "=================================================="
)

comandos_registrados = sorted(
    (
        command.name
        for command in bot.commands
    ),
    key=str.lower
)

for comando in comandos_registrados:

    logger.info(
        "   !%s",
        comando
    )

logger.info(
    "Total de comandos: %s",
    len(comandos_registrados)
)


# ============================================================
# 16. EVENTO ON_READY
# ============================================================

@bot.event
async def on_ready():

    global bot_listo

    reconexion = bot_listo

    bot_listo = True

    logger.info(
        "=================================================="
    )

    if reconexion:

        logger.info(
            "🔄 Discord ha vuelto a ejecutar on_ready."
        )

    else:

        logger.info(
            "🟢 Primera conexión de Discord."
        )

    logger.info(
        "🦊 BOT CONECTADO: %s",
        bot.user
    )

    logger.info(
        "💖 [Noah]: ¡El muchacho ya está en línea y brillando en el chat, mi tigre!"
    )

    logger.info(
        "🆔 ID: %s",
        bot.user.id
    )

    logger.info(
        "🌐 Servidores: %s",
        len(bot.guilds)
    )

    logger.info(
        "👥 Usuarios visibles: %s",
        len(bot.users)
    )

    logger.info(
        "📡 Latencia: %sms",
        round(
            bot.latency * 1000
        )
    )

    logger.info(
        "=================================================="
    )

    for nombre, estado in (
        sistemas_cargados.items()
    ):

        if estado:

            logger.info(
                "✅ %s: cargado",
                nombre
            )

        else:

            logger.error(
                "❌ %s: ERROR",
                nombre
            )

    logger.info(
        "=================================================="
    )

    logger.info(
        "🦊 Foxy está operativo."
    )

    logger.info(
        "🔊 Voice Auto está preparado."
    )

    logger.info(
        "🟣 Twitch está preparado."
    )

    logger.info(
        "🤖 OpenAI está preparado."
    )

    logger.info(
        "=================================================="
    )


# ============================================================
# 17. CONEXIÓN
# ============================================================

@bot.event
async def on_connect():

    logger.info(
        "📡 Conexión con Discord establecida."
    )


# ============================================================
# 18. ENTRADA DE MIEMBROS
# ============================================================

@bot.event
async def on_member_join(
    member
):

    canales_preferidos = [
        "general",
        "bienvenida",
        "lanzamiento"
    ]

    for channel in (
        member.guild.text_channels
    ):

        if channel.name.lower() not in (
            canales_preferidos
        ):
            continue

        try:

            await channel.send(
                "¡Atención tripulación de Foxy! 🔥\n"
                f"¡{member.mention} acaba de entrar "
                "al servidor oficial!\n\n"
                "🦊 ¡Bienvenido/a!\n"
                "💰 Reclama tus monedas con `!daily`.\n"
                "🎮 Usa `!ayuda` para conocer los sistemas."
            )

        except discord.Forbidden:

            logger.warning(
                "Sin permisos para escribir en #%s",
                channel.name
            )

        except discord.HTTPException as error:

            logger.error(
                "Error de Discord en bienvenida: %s",
                error
            )

        break


# ============================================================
# 19. SALIDA DE MIEMBROS
# ============================================================

@bot.event
async def on_member_remove(
    member
):

    canales_preferidos = [
        "general",
        "despedidas",
        "salidas"
    ]

    for channel in (
        member.guild.text_channels
    ):

        if channel.name.lower() not in (
            canales_preferidos
        ):
            continue

        try:

            await channel.send(
                f"💀 **{member.name}** "
                "ha abandonado la comunidad.\n"
                "F por los caídos en combate."
            )

        except discord.Forbidden:

            logger.warning(
                "Sin permisos para escribir en #%s",
                channel.name
            )

        except discord.HTTPException as error:

            logger.error(
                "Error enviando despedida: %s",
                error
            )

        break


# ============================================================
# 20. ON_MESSAGE
# ============================================================

@bot.event
async def on_message(
    message
):

    if message.author.bot:
        return

    estadisticas_bot[
        "mensajes"
    ] += 1

    if message.guild is None:

        try:

            await bot.process_commands(
                message
            )

        except Exception as error:

            estadisticas_bot[
                "errores"
            ] += 1

            logger.error(
                "Error procesando comando DM: %s",
                error
            )

        return

    user_id = message.author.id

    datos = obtener_nivel_legacy(
        user_id
    )

    ganancia_xp = random.randint(
        XP_MIN,
        XP_MAX
    )

    datos["xp"] += ganancia_xp

    estadisticas_bot[
        "xp_otorgado"
    ] += ganancia_xp

    nivel_actual = datos[
        "nivel"
    ]

    xp_necesaria = nivel_necesario(
        nivel_actual
    )

    if datos["xp"] >= xp_necesaria:

        datos["nivel"] += 1

        datos["xp"] -= xp_necesaria

        nuevo_nivel = datos[
            "nivel"
        ]

        try:

            await message.channel.send(
                f"🎉 ¡Enhorabuena "
                f"{message.author.mention}!\n\n"
                f"⭐ Has alcanzado el "
                f"**nivel {nuevo_nivel}**.\n"
                "📈 Sigue participando para subir aún más."
            )

        except discord.HTTPException:

            pass

    try:

        await bot.process_commands(
            message
        )

    except Exception as error:

        estadisticas_bot[
            "errores"
        ] += 1

        logger.error(
            "Error procesando comando: %s",
            error
        )

        traceback.print_exc()


# ============================================================
# 21. CONTADOR DE COMANDOS
# ============================================================

@bot.event
async def on_command(
    ctx
):

    estadisticas_bot[
        "comandos"
    ] += 1


# ============================================================
# 22. HOLA
# ============================================================

@legacy_command()
async def hola(ctx):

    await ctx.send(
        "¡Arrrgh! ¡Saludos, grumete! 🦊\n"
        "Foxy está operativo al 100% "
        "con todos los sistemas listos."
    )


# ============================================================
# 23. PING
# ============================================================

@legacy_command()
async def ping(ctx):

    latencia = round(
        bot.latency * 1000
    )

    await ctx.send(
        f"🏓 Pong\n"
        f"📡 Latencia: **{latencia} ms**"
    )


# ============================================================
# 24. BOTINFO
# ============================================================

@legacy_command()
async def botinfo(ctx):

    uptime = tiempo_humano(
        time.time()
        -
        estadisticas_bot["inicio"]
    )

    embed = discord.Embed(
        title="🦊 DC_Foxy_Bot",
        description=BOT_DESCRIPTION,
        color=discord.Color.orange()
    )

    embed.add_field(
        name="📦 Versión",
        value=f"`{BOT_VERSION}`",
        inline=True
    )

    embed.add_field(
        name="🐍 Tecnología",
        value="Python + discord.py",
        inline=True
    )

    embed.add_field(
        name="🌐 Servidores",
        value=str(
            len(bot.guilds)
        ),
        inline=True
    )

    embed.add_field(
        name="⏱️ Uptime",
        value=uptime,
        inline=True
    )

    embed.add_field(
        name="📡 Latencia",
        value=(
            f"{round(bot.latency * 1000)} ms"
        ),
        inline=True
    )

    embed.add_field(
        name="🎮 Sistemas",
        value=(
            "🦊 Foxy Core\n"
            "🎮 RPG\n"
            "💰 Economía\n"
            "🎒 Inventario\n"
            "🛒 Tienda\n"
            "🎮 Game Client\n"
            "🎵 Music\n"
            "🎙️ TTS\n"
            "🔊 Voice Auto\n"
            "🟣 Twitch\n"
            "🤖 OpenAI\n"
            "🛡️ Seguridad\n"
            "📋 Logs\n"
            "🤖 Foxy AI"
        ),
        inline=False
    )

    await ctx.send(
        embed=embed
    )


# ============================================================
# 25. SERVERINFO
# ============================================================

@legacy_command()
async def serverinfo(ctx):

    guild = ctx.guild

    if guild is None:

        await ctx.send(
            "❌ Este comando solo funciona "
            "en un servidor."
        )

        return

    fecha = guild.created_at.strftime(
        "%d/%m/%Y"
    )

    embed = discord.Embed(
        title=f"🏰 {guild.name}",
        color=discord.Color.orange()
    )

    embed.add_field(
        name="👑 Dueño",
        value=str(
            guild.owner
        ),
        inline=True
    )

    embed.add_field(
        name="👥 Miembros",
        value=str(
            guild.member_count
        ),
        inline=True
    )

    embed.add_field(
        name="📅 Creado",
        value=fecha,
        inline=True
    )

    embed.add_field(
        name="🆔 ID",
        value=f"`{guild.id}`",
        inline=True
    )

    embed.add_field(
        name="💬 Canales",
        value=str(
            len(guild.channels)
        ),
        inline=True
    )

    embed.add_field(
        name="😀 Emojis",
        value=str(
            len(guild.emojis)
        ),
        inline=True
    )

    await ctx.send(
        embed=embed
    )


# ============================================================
# 26. AVATAR
# ============================================================

@legacy_command()
async def avatar(
    ctx,
    miembro: discord.Member = None
):

    miembro = miembro or ctx.author

    embed = discord.Embed(
        title=(
            f"🖼️ Avatar de {miembro.name}"
        ),
        color=discord.Color.orange()
    )

    embed.set_image(
        url=miembro.display_avatar.url
    )

    embed.set_footer(
        text=f"ID: {miembro.id}"
    )

    await ctx.send(
        embed=embed
    )


# ============================================================
# 27. PERFIL
# ============================================================

@legacy_command()
async def perfil(
    ctx,
    miembro: discord.Member = None
):

    miembro = miembro or ctx.author

    datos_xp = obtener_nivel_legacy(
        miembro.id
    )

    datos_economia = (
        obtener_economia_legacy(
            miembro.id
        )
    )

    fecha_ingreso = (
        miembro.joined_at.strftime(
            "%d/%m/%Y"
        )
        if miembro.joined_at
        else "Desconocida"
    )

    embed = discord.Embed(
        title=(
            f"📋 Perfil de "
            f"{miembro.display_name}"
        ),
        color=discord.Color.orange()
    )

    embed.set_thumbnail(
        url=miembro.display_avatar.url
    )

    embed.add_field(
        name="🆔 ID",
        value=f"`{miembro.id}`",
        inline=False
    )

    embed.add_field(
        name="📅 Entrada",
        value=fecha_ingreso,
        inline=True
    )

    embed.add_field(
        name="⭐ Nivel",
        value=str(
            datos_xp["nivel"]
        ),
        inline=True
    )

    embed.add_field(
        name="✨ XP",
        value=str(
            datos_xp["xp"]
        ),
        inline=True
    )

    embed.add_field(
        name="💰 Monedas legacy",
        value=str(
            datos_economia["monedas"]
        ),
        inline=True
    )

    await ctx.send(
        embed=embed
    )


# ============================================================
# 28. BALANCE
# ============================================================

@legacy_command()
async def balance(
    ctx,
    miembro: discord.Member = None
):

    miembro = miembro or ctx.author

    datos = obtener_economia_legacy(
        miembro.id
    )

    await ctx.send(
        f"💰 El monedero de "
        f"**{miembro.display_name}** contiene "
        f"**{datos['monedas']} monedas** 🪙."
    )


# ============================================================
# 29. DIARIO
# ============================================================

@legacy_command()
async def diario(ctx):

    user_id = ctx.author.id

    datos = obtener_economia_legacy(
        user_id
    )

    datos["monedas"] += 250

    await ctx.send(
        f"🎁 ¡Has reclamado "
        f"**250 monedas**!\n"
        f"💰 Saldo legacy: "
        f"**{datos['monedas']} monedas** 🪙."
    )


# ============================================================
# 30. TRABAJAR
# ============================================================

@legacy_command()
async def trabajar(ctx):

    user_id = ctx.author.id

    datos = obtener_economia_legacy(
        user_id
    )

    ganancia = random.randint(
        30,
        90
    )

    labores = [
        "configurando redes informáticas",
        "optimizando sistemas",
        "diseñando overlays para streaming",
        "programando scripts en Python",
        "gestionando servidores",
        "revisando el código de Foxy",
        "arreglando bugs",
        "moderando el servidor",
        "entrenando a la IA de Foxy",
        "haciendo mantenimiento del servidor"
    ]

    trabajo = random.choice(
        labores
    )

    datos["monedas"] += ganancia

    await ctx.send(
        f"💼 **{ctx.author.name}** ha estado "
        f"{trabajo} y ha conseguido "
        f"**{ganancia} monedas** 🪙."
    )


# ============================================================
# 31. NIVEL
# ============================================================

@legacy_command()
async def nivel(
    ctx,
    miembro: discord.Member = None
):

    miembro = miembro or ctx.author

    datos = obtener_nivel_legacy(
        miembro.id
    )

    actual = datos[
        "xp"
    ]

    necesario = nivel_necesario(
        datos["nivel"]
    )

    barra = texto_barra(
        actual,
        necesario,
        12
    )

    await ctx.send(
        f"⭐ **Nivel de "
        f"{miembro.display_name}**\n\n"
        f"🏆 Nivel: **{datos['nivel']}**\n"
        f"✨ XP: **{actual}/{necesario}**\n"
        f"{barra}"
    )


# ============================================================
# 32. DADO
# ============================================================

@legacy_command()
async def dado(
    ctx,
    caras: int = 6
):

    if caras < 2:

        await ctx.send(
            "❌ El dado debe tener "
            "al menos 2 caras."
        )

        return

    if caras > 100000:

        await ctx.send(
            "❌ Máximo 100000 caras."
        )

        return

    resultado = random.randint(
        1,
        caras
    )

    await ctx.send(
        f"🎲 **{ctx.author.display_name}** "
        f"lanza un dado de **{caras}** caras.\n\n"
        f"🎯 Resultado: **{resultado}**"
    )


# ============================================================
# 33. MONEDA
# ============================================================

@legacy_command()
async def moneda(ctx):

    resultado = random.choice(
        [
            "CARA",
            "CRUZ"
        ]
    )

    emoji = (
        "🙂"
        if resultado == "CARA"
        else
        "🌙"
    )

    await ctx.send(
        f"🪙 **{ctx.author.display_name}**\n"
        f"{emoji} **{resultado}**"
    )


# ============================================================
# 34. BOLA 8
# ============================================================

@legacy_command(
    name="bola8"
)
async def bola8(
    ctx,
    *,
    pregunta: str
):

    respuestas = [
        "🟢 Sí, totalmente.",
        "🟢 Las señales apuntan a que sí.",
        "🟢 Definitivamente.",
        "🟡 Las probabilidades son altas.",
        "🟡 Puede ser.",
        "🟡 No está claro.",
        "🟠 Mejor vuelve a preguntar.",
        "🔴 No parece probable.",
        "🔴 Ni lo sueñes.",
        "🔴 Las perspectivas no son favorables.",
        "🔴 Rotundamente no.",
        "🎱 Foxy necesita más datos.",
        "🦊 Foxy dice que confíes en tu instinto."
    ]

    respuesta = random.choice(
        respuestas
    )

    await ctx.send(
        f"🎱 **Pregunta:**\n"
        f"{pregunta}\n\n"
        f"🔮 **Respuesta:**\n"
        f"{respuesta}"
    )


# ============================================================
# 35. CHISTE
# ============================================================

@legacy_command()
async def chiste(ctx):

    repertorio = [
        "¿Qué hace un mago en una granja? "
        "¡Abracadabra cabras!",

        "Hay 10 tipos de personas: "
        "las que entienden binario y las que no.",

        "¿Por qué los programadores odian el calor? "
        "Porque aparecen bugs.",

        "Un programador entra a un bar... "
        "pide 1 cerveza, 0 cervezas y -1 cervezas.",

        "Foxy intentó contar hasta infinito. "
        "Todavía sigue por el camino."
    ]

    await ctx.send(
        random.choice(
            repertorio
        )
    )


# ============================================================
# 36. CHISTE OSCURO
# ============================================================

@legacy_command()
async def chisteoscuro(ctx):

    repertorio = [
        "Mi PC tiene más problemas que yo "
        "y encima no puede ir al psicólogo.",

        "Mi WiFi tiene una relación tóxica conmigo: "
        "desaparece cuando más lo necesito.",

        "El servidor dijo que estaba estable. "
        "Cinco segundos después conoció a la gravedad.",

        "Mi código no tiene bugs. "
        "Tiene funcionalidades sorpresa."
    ]

    await ctx.send(
        random.choice(
            repertorio
        )
    )


# ============================================================
# 37. AMOR
# ============================================================

@legacy_command()
async def amor(
    ctx,
    persona1: str,
    persona2: str = None
):

    if persona2 is None:

        persona1, persona2 = (
            ctx.author.name,
            persona1
        )

    especiales = {
        "foxy",
        "foxy2003tv_",
        "foxy20850",
        "adrian"
    }

    infinitos = {
        "steffie",
        "stephi"
    }

    p1 = persona1.lower()
    p2 = persona2.lower()

    if (
        p1 in infinitos
        or
        p2 in infinitos
    ):

        porcentaje = 1000

    elif (
        p1 in especiales
        or
        p2 in especiales
    ):

        porcentaje = random.randint(
            85,
            100
        )

    else:

        porcentaje = random.randint(
            0,
            100
        )

    if porcentaje >= 1000:

        comentario = (
            "🌟 ¡AMOR INFINITO DETECTADO!"
        )

    elif porcentaje > 80:

        comentario = (
            "🔥 ¡Una química absoluta!"
        )

    elif porcentaje > 50:

        comentario = (
            "💖 Hay posibilidades."
        )

    elif porcentaje > 20:

        comentario = (
            "🟡 Hay algo de química."
        )

    else:

        comentario = (
            "💀 Mejor ni intentarlo."
        )

    await ctx.send(
        f"💘 **Compatibilidad Amorosa** 💘\n\n"
        f"**{persona1}** ❤️ **{persona2}**\n"
        f"💯 Compatibilidad: **{porcentaje}%**\n\n"
        f"{comentario}"
    )


# ============================================================
# 38. PESCA
# ============================================================

@legacy_command()
async def pesca(ctx):

    capturas = [
        ("👢 Una bota vieja", 1),
        ("🐟 Una sardina", 3),
        ("🐠 Un pez tropical", 5),
        ("🦀 Un cangrejo", 8),
        ("🐡 Un pez globo", 10),
        ("🐙 Un pulpo", 12),
        ("🦈 Un pez grande", 15),
        ("🐋 Una criatura marina gigante", 20),
        ("✨ Un pez legendario", 30),
    ]

    pez, estrellas = random.choice(
        capturas
    )

    await ctx.send(
        f"🎣 **{ctx.author.display_name}** "
        f"ha pescado:\n\n"
        f"{pez}\n"
        f"⭐ Valor: **{estrellas}**"
    )


# ============================================================
# 39. INVERTIR
# ============================================================

@legacy_command()
async def invertir(
    ctx,
    cantidad: int
):

    if cantidad <= 0:

        await ctx.send(
            "❌ La cantidad debe ser positiva."
        )

        return

    if cantidad > 1000000:

        await ctx.send(
            "❌ La cantidad máxima es 1.000.000."
        )

        return

    resultado = random.choice(
        [
            "ganar",
            "perder",
            "gran_ganar",
            "gran_perder"
        ]
    )

    if resultado == "ganar":

        ganancia = cantidad

        await ctx.send(
            f"📈 ¡La inversión salió bien!\n"
            f"💰 Ganancia: **{ganancia} monedas**."
        )

    elif resultado == "gran_ganar":

        ganancia = cantidad * 2

        await ctx.send(
            f"🚀 ¡INVERSIÓN LEGENDARIA!\n"
            f"💰 Ganancia: **{ganancia} monedas**."
        )

    elif resultado == "gran_perder":

        perdida = cantidad * 2

        await ctx.send(
            f"💥 ¡Desastre financiero!\n"
            f"📉 Pérdida teórica: **{perdida} monedas**."
        )

    else:

        await ctx.send(
            f"📉 La inversión salió mal.\n"
            f"💸 Perdiste **{cantidad} monedas**."
        )


# ============================================================
# 40. COINFLIP
# ============================================================

@legacy_command()
async def coinflip(
    ctx,
    eleccion: str,
    apuesta: int
):

    if apuesta <= 0:

        await ctx.send(
            "❌ La apuesta debe ser positiva."
        )

        return

    eleccion = eleccion.lower()

    traducciones = {
        "cara": "cara",
        "car": "cara",
        "heads": "cara",
        "cruz": "cruz",
        "tails": "cruz"
    }

    eleccion = traducciones.get(
        eleccion
    )

    if eleccion is None:

        await ctx.send(
            "❌ Elige `cara` o `cruz`."
        )

        return

    resultado = random.choice(
        [
            "cara",
            "cruz"
        ]
    )

    if resultado == eleccion:

        await ctx.send(
            f"🪙 La moneda gira...\n\n"
            f"🎯 Salió: **{resultado.upper()}**\n"
            f"🎉 ¡Has acertado!"
        )

    else:

        await ctx.send(
            f"🪙 La moneda gira...\n\n"
            f"🎯 Salió: **{resultado.upper()}**\n"
            f"💀 Has fallado."
        )


# ============================================================
# 41. REGALO DE MONEDAS
# ============================================================

@legacy_command()
async def regalomonedas(
    ctx,
    miembro: discord.Member,
    cantidad: int
):

    if cantidad <= 0:

        await ctx.send(
            "❌ La cantidad debe ser positiva."
        )

        return

    if cantidad > 1000000:

        await ctx.send(
            "❌ Cantidad demasiado grande."
        )

        return

    receptor = obtener_economia_legacy(
        miembro.id
    )

    receptor["monedas"] += cantidad

    await ctx.send(
        f"🎁 **{ctx.author.display_name}** "
        f"ha regalado **{cantidad} monedas** "
        f"a **{miembro.display_name}**."
    )


# ============================================================
# 42. PIEDRA PAPEL TIJERA
# ============================================================

@legacy_command(
    name="piedrapapeltijera"
)
async def piedrapapeltijera(
    ctx,
    eleccion: str
):

    opciones = [
        "piedra",
        "papel",
        "tijera"
    ]

    eleccion = eleccion.lower()

    if eleccion not in opciones:

        await ctx.send(
            "❌ Elige: "
            "`piedra`, `papel` o `tijera`."
        )

        return

    bot_eleccion = random.choice(
        opciones
    )

    if eleccion == bot_eleccion:

        resultado = "🤝 ¡Empate!"

    elif (
        eleccion == "piedra"
        and bot_eleccion == "tijera"
    ) or (
        eleccion == "papel"
        and bot_eleccion == "piedra"
    ) or (
        eleccion == "tijera"
        and bot_eleccion == "papel"
    ):

        resultado = "🎉 ¡Has ganado!"

    else:

        resultado = "💀 ¡Foxy ha ganado!"

    await ctx.send(
        f"🎮 **Piedra, Papel o Tijera**\n\n"
        f"👤 Tú: **{eleccion}**\n"
        f"🦊 Foxy: **{bot_eleccion}**\n\n"
        f"{resultado}"
    )


# ============================================================
# 43. BESO
# ============================================================

@legacy_command()
async def beso(
    ctx,
    miembro: discord.Member
):

    await ctx.send(
        f"💋 **{ctx.author.display_name}** "
        f"le da un beso a "
        f"**{miembro.display_name}**."
    )


# ============================================================
# 44. ABRAZO
# ============================================================

@legacy_command()
async def abrazo(
    ctx,
    miembro: discord.Member
):

    await ctx.send(
        f"🤗 **{ctx.author.display_name}** "
        f"abraza a "
        f"**{miembro.display_name}**."
    )


# ============================================================
# 45. KILL
# ============================================================

@legacy_command()
async def kill(
    ctx,
    miembro: discord.Member
):

    frases = [
        "ha sido derrotado por Foxy 💀",
        "ha recibido un crítico de 9999 de daño 💥",
        "ha caído en combate 🪦",
        "ha sido enviado al respawn 🔄",
        "ha sido destruido por una ardilla 🐿️",
        "ha sido víctima de un bug legendario 🐛"
    ]

    await ctx.send(
        f"☠️ **{miembro.display_name}** "
        f"{random.choice(frases)}."
    )


# ============================================================
# 46. EXPULSAR
# ============================================================

@legacy_command(
    name="expulsar"
)
async def expulsar(
    ctx,
    miembro: discord.Member,
    *,
    motivo: str = "Sin motivo especificado"
):

    if not ctx.guild:

        await ctx.send(
            "❌ Solo puede utilizarse "
            "en un servidor."
        )

        return

    if not ctx.author.guild_permissions.kick_members:

        await ctx.send(
            "❌ No tienes permiso para expulsar miembros."
        )

        return

    if miembro == ctx.author:

        await ctx.send(
            "❌ No puedes expulsarte a ti mismo."
        )

        return

    if miembro == ctx.guild.owner:

        await ctx.send(
            "❌ No puedes expulsar al dueño del servidor."
        )

        return

    try:

        await miembro.kick(
            reason=motivo
        )

        await ctx.send(
            f"👢 **{miembro}** ha sido expulsado.\n"
            f"📝 Motivo: {motivo}"
        )

    except discord.Forbidden:

        await ctx.send(
            "❌ Discord no permite expulsar a ese usuario. "
            "Comprueba la jerarquía de roles."
        )

    except discord.HTTPException as error:

        logger.error(
            "Error expulsando miembro: %s",
            error
        )

        await ctx.send(
            "❌ Discord rechazó la expulsión."
        )


# ============================================================
# 47. BAN
# ============================================================

@legacy_command(
    name="ban"
)
async def ban(
    ctx,
    miembro: discord.Member,
    *,
    motivo: str = "Sin motivo especificado"
):

    if not ctx.guild:

        await ctx.send(
            "❌ Solo puede utilizarse "
            "en un servidor."
        )

        return

    if not ctx.author.guild_permissions.ban_members:

        await ctx.send(
            "❌ No tienes permiso para banear miembros."
        )

        return

    if miembro == ctx.author:

        await ctx.send(
            "❌ No puedes banearte a ti mismo."
        )

        return

    if miembro == ctx.guild.owner:

        await ctx.send(
            "❌ No puedes banear al dueño."
        )

        return

    try:

        await miembro.ban(
            reason=motivo,
            delete_message_days=0
        )

        await ctx.send(
            f"🔨 **{miembro}** ha sido baneado.\n"
            f"📝 Motivo: {motivo}"
        )

    except discord.Forbidden:

        await ctx.send(
            "❌ Discord no permite banear a ese usuario. "
            "Comprueba la jerarquía de roles."
        )

    except discord.HTTPException:

        await ctx.send(
            "❌ Discord rechazó el baneo."
        )


# ============================================================
# 48. LIMPIAR
# ============================================================

@legacy_command(
    name="limpiar"
)
async def limpiar(
    ctx,
    cantidad: int = 10
):

    if not ctx.guild:

        await ctx.send(
            "❌ Solo funciona en servidores."
        )

        return

    if not ctx.author.guild_permissions.manage_messages:

        await ctx.send(
            "❌ Necesitas permiso para gestionar mensajes."
        )

        return

    if cantidad < 1:

        await ctx.send(
            "❌ La cantidad mínima es 1."
        )

        return

    if cantidad > 100:

        await ctx.send(
            "❌ Máximo 100 mensajes por operación."
        )

        return

    try:

        borrados = await ctx.channel.purge(
            limit=cantidad + 1
        )

        aviso = await ctx.send(
            f"🧹 Se han eliminado "
            f"**{len(borrados) - 1} mensajes**."
        )

        await asyncio.sleep(
            4
        )

        try:

            await aviso.delete()

        except discord.HTTPException:

            pass

    except discord.Forbidden:

        await ctx.send(
            "❌ No tengo permisos suficientes."
        )

    except discord.HTTPException:

        await ctx.send(
            "❌ Discord rechazó la operación."
        )


# ============================================================
# 49. SORTEO DISCORD
# ============================================================

@legacy_command(
    name="sorteo"
)
async def sorteo(
    ctx,
    minutos: int,
    *,
    premio: str
):

    if minutos < 1:

        await ctx.send(
            "❌ El sorteo debe durar "
            "al menos 1 minuto."
        )

        return

    if minutos > 10080:

        await ctx.send(
            "❌ El máximo es de 7 días."
        )

        return

    mensaje = await ctx.send(
        "🎉 **SORTEO** 🎉\n\n"
        f"🏆 Premio: **{premio}**\n"
        f"⏱️ Duración: **{minutos} minutos**\n\n"
        "🎟️ Reacciona con 🎉 para participar."
    )

    try:

        await mensaje.add_reaction(
            "🎉"
        )

    except discord.HTTPException:

        pass

    await asyncio.sleep(
        minutos * 60
    )

    try:

        mensaje_actualizado = (
            await ctx.channel.fetch_message(
                mensaje.id
            )
        )

    except discord.HTTPException:

        return

    participantes = []

    for reaction in (
        mensaje_actualizado.reactions
    ):

        if str(
            reaction.emoji
        ) != "🎉":
            continue

        try:

            usuarios = [
                usuario
                async for usuario
                in reaction.users()
            ]

            participantes.extend(
                [
                    usuario
                    for usuario in usuarios
                    if not usuario.bot
                ]
            )

        except discord.HTTPException:

            pass

    participantes = list(
        {
            usuario.id: usuario
            for usuario in participantes
        }.values()
    )

    if not participantes:

        await ctx.send(
            "😢 El sorteo ha terminado "
            "sin participantes."
        )

        return

    ganador = random.choice(
        participantes
    )

    await ctx.send(
        "🎊 **SORTEO TERMINADO** 🎊\n\n"
        f"🏆 Premio: **{premio}**\n"
        f"👑 Ganador: {ganador.mention}\n\n"
        "🦊 ¡Enhorabuena!"
    )


# ============================================================
# 50. ENCUESTA
# ============================================================

@legacy_command(
    name="encuesta"
)
async def encuesta(
    ctx,
    *,
    pregunta: str
):

    if not pregunta.strip():

        await ctx.send(
            "❌ Debes escribir una pregunta."
        )

        return

    try:

        await ctx.message.delete()

    except discord.Forbidden:

        pass

    except discord.NotFound:

        pass

    mensaje = await ctx.send(
        "📊 **ENCUESTA**\n\n"
        f"❓ **{pregunta}**\n\n"
        "👍 = Sí\n"
        "👎 = No"
    )

    try:

        await mensaje.add_reaction(
            "👍"
        )

        await mensaje.add_reaction(
            "👎"
        )

    except discord.HTTPException:

        pass


# ============================================================
# 51. AYUDA
# ============================================================

if bot.get_command(
    "ayuda"
) is None:

    @bot.command(
        name="ayuda",
        aliases=[
            "help",
            "comandos"
        ]
    )
    async def ayuda(ctx):

        embed = discord.Embed(
            title="🦊 Ayuda de DC_Foxy_Bot",
            description=(
                "Sistema central de comandos de Foxy.\n"
                "Los comandos disponibles pueden variar "
                "según los módulos instalados."
            ),
            color=discord.Color.orange()
        )

        embed.add_field(
            name="🦊 Foxy",
            value=(
                "`!foxy`\n"
                "`!perfil`\n"
                "`!stats`\n"
                "`!resumen`"
            ),
            inline=False
        )

        embed.add_field(
            name="💰 Economía",
            value=(
                "`!saldo`\n"
                "`!daily`\n"
                "`!trabajar`\n"
                "`!pagar`\n"
                "`!balance`\n"
                "`!diario`"
            ),
            inline=False
        )

        embed.add_field(
            name="🎒 Inventario",
            value=(
                "`!inventario`\n"
                "`!usar`"
            ),
            inline=False
        )

        embed.add_field(
            name="🛒 Tienda",
            value=(
                "`!tienda`\n"
                "`!comprar`\n"
                "`!precio`"
            ),
            inline=False
        )

        embed.add_field(
            name="⭐ RPG",
            value=(
                "`!nivel`\n"
                "`!stats`\n"
                "`!resumen`"
            ),
            inline=False
        )

        embed.add_field(
            name="🎵 Música",
            value=(
                "`!p <canción>` — Añadir canción\n"
                "`!pl <playlist>` — Añadir playlist\n"
                "`!a` — Canción actual\n"
                "`!n` — Siguiente\n"
                "`!b` — Anterior\n"
                "`!s` — Detener\n"
                "`!leave` — Salir del canal"
            ),
            inline=False
        )

        embed.add_field(
            name="🎙️ TTS",
            value=(
                "Foxy lee automáticamente los mensajes "
                "de usuarios que estén en un canal de voz."
            ),
            inline=False
        )

        embed.add_field(
            name="🔊 Voice Auto",
            value=(
                "Foxy entra automáticamente a un canal "
                "de voz cuando entra un usuario.\n"
                "Si el canal queda vacío, espera "
                "**60 segundos** y se desconecta."
            ),
            inline=False
        )

        embed.add_field(
            name="🟣 Twitch",
            value=(
                "`!twitch` — Estado de la integración\n"
                "Los comandos de chat de Twitch se "
                "gestionan independientemente de Discord."
            ),
            inline=False
        )

        embed.add_field(
            name="🤖 OpenAI",
            value=(
                "`!ia <pregunta>` — Hablar con la IA\n"
                "`!ai <pregunta>` — Alias de IA\n"
                "`!openai <pregunta>` — Alias de OpenAI\n"
                "`!iaestado` — Estado de OpenAI"
            ),
            inline=False
        )

        embed.add_field(
            name="🎮 Game Client",
            value=(
                "`!juego lista`\n"
                "`!juego conectar <juego>`\n"
                "`!juego desconectar`\n"
                "`!juego estado`\n"
                "`!juego chat <mensaje>`\n"
                "`!juego mover <direccion>`"
            ),
            inline=False
        )

        embed.add_field(
            name="🎮 Juegos",
            value=(
                "`!dado`\n"
                "`!moneda`\n"
                "`!bola8`\n"
                "`!piedrapapeltijera`\n"
                "`!pesca`\n"
                "`!jugar`\n"
                "`!jueguito`"
            ),
            inline=False
        )

        embed.add_field(
            name="😂 Diversión",
            value=(
                "`!chiste`\n"
                "`!chisteoscuro`\n"
                "`!amor`\n"
                "`!beso`\n"
                "`!abrazo`\n"
                "`!kill`"
            ),
            inline=False
        )

        embed.add_field(
            name="🛡️ Moderación",
            value=(
                "`!expulsar`\n"
                "`!ban`\n"
                "`!limpiar`\n"
                "`!sorteo`\n"
                "`!encuesta`"
            ),
            inline=False
        )

        embed.add_field(
            name="🔧 Sistema",
            value=(
                "`!hola`\n"
                "`!ping`\n"
                "`!botinfo`\n"
                "`!serverinfo`\n"
                "`!avatar`"
            ),
            inline=False
        )

        embed.set_footer(
            text=(
                f"DC_Foxy_Bot {BOT_VERSION} • "
                f"{len(bot.commands)} comandos registrados"
            )
        )

        await ctx.send(
            embed=embed
        )


# ============================================================
# 52. ESTADO
# ============================================================

if bot.get_command(
    "estado"
) is None:

    @bot.command(
        name="estado",
        aliases=[
            "status",
            "health"
        ]
    )
    async def estado(ctx):

        embed = discord.Embed(
            title="🦊 Estado de Foxy",
            color=discord.Color.green()
        )

        estado_bot = (
            "🟢 ONLINE"
            if bot_listo
            else
            "🟡 INICIANDO"
        )

        embed.add_field(
            name="🤖 Bot",
            value=estado_bot,
            inline=True
        )

        embed.add_field(
            name="📡 Latencia",
            value=(
                f"{round(bot.latency * 1000)} ms"
            ),
            inline=True
        )

        embed.add_field(
            name="🌐 Servidores",
            value=str(
                len(bot.guilds)
            ),
            inline=True
        )

        cargados = sum(
            1
            for valor
            in sistemas_cargados.values()
            if valor
        )

        total = len(
            sistemas_cargados
        )

        embed.add_field(
            name="⚙️ Módulos",
            value=f"{cargados}/{total}",
            inline=True
        )

        embed.add_field(
            name="📜 Comandos",
            value=str(
                len(bot.commands)
            ),
            inline=True
        )

        embed.add_field(
            name="💬 Mensajes",
            value=str(
                estadisticas_bot[
                    "mensajes"
                ]
            ),
            inline=True
        )

        embed.add_field(
            name="⌨️ Comandos usados",
            value=str(
                estadisticas_bot[
                    "comandos"
                ]
            ),
            inline=True
        )

        embed.add_field(
            name="❌ Errores",
            value=str(
                estadisticas_bot[
                    "errores"
                ]
            ),
            inline=True
        )

        embed.add_field(
            name="⏱️ Uptime",
            value=tiempo_humano(
                time.time()
                -
                estadisticas_bot[
                    "inicio"
                ]
            ),
            inline=True
        )

        await ctx.send(
            embed=embed
        )


# ============================================================
# 53. SISTEMAS
# ============================================================

if bot.get_command(
    "sistemas"
) is None:

    @bot.command(
        name="sistemas"
    )
    async def sistemas(ctx):

        embed = discord.Embed(
            title="⚙️ Sistemas de Foxy",
            color=discord.Color.orange()
        )

        if not sistemas_cargados:

            embed.description = (
                "No se han registrado módulos."
            )

        else:

            for nombre, estado in (
                sistemas_cargados.items()
            ):

                simbolo = (
                    "🟢"
                    if estado
                    else
                    "🔴"
                )

                embed.add_field(
                    name=f"{simbolo} {nombre}",
                    value=(
                        "Funcionando"
                        if estado
                        else
                        "Error al cargar"
                    ),
                    inline=True
                )

        await ctx.send(
            embed=embed
        )


# ============================================================
# 54. LISTA
# ============================================================

if bot.get_command(
    "lista"
) is None:

    @bot.command(
        name="lista"
    )
    async def lista(ctx):

        comandos = sorted(
            (
                command.name
                for command in bot.commands
                if not command.hidden
            ),
            key=str.lower
        )

        bloques = []

        bloque_actual = ""

        for comando in comandos:

            linea = (
                f"`!{comando}` "
            )

            if len(
                bloque_actual + linea
            ) > 900:

                bloques.append(
                    bloque_actual
                )

                bloque_actual = ""

            bloque_actual += linea

        if bloque_actual:

            bloques.append(
                bloque_actual
            )

        embed = discord.Embed(
            title="📜 Comandos disponibles",
            description=(
                f"Total: **{len(comandos)}**"
            ),
            color=discord.Color.orange()
        )

        for indice, bloque in enumerate(
            bloques[:10],
            start=1
        ):

            embed.add_field(
                name=f"📦 Página {indice}",
                value=bloque,
                inline=False
            )

        await ctx.send(
            embed=embed
        )


# ============================================================
# 55. ERROR GLOBAL
# ============================================================

@bot.event
async def on_command_error(
    ctx,
    error
):

    estadisticas_bot[
        "errores"
    ] += 1

    if isinstance(
        error,
        commands.CommandInvokeError
    ):

        original = error.original

    else:

        original = error

    if isinstance(
        original,
        commands.CommandNotFound
    ):

        return

    if isinstance(
        original,
        commands.DisabledCommand
    ):

        await enviar_seguro(
            ctx,
            "🚫 Este comando está deshabilitado."
        )

        return

    if isinstance(
        original,
        commands.MissingPermissions
    ):

        permisos = ", ".join(
            original.missing_permissions
        )

        await enviar_seguro(
            ctx,
            "❌ No tienes permisos suficientes.\n"
            f"🔐 Requeridos: `{permisos}`"
        )

        return

    if isinstance(
        original,
        commands.BotMissingPermissions
    ):

        permisos = ", ".join(
            original.missing_permissions
        )

        await enviar_seguro(
            ctx,
            "❌ No tengo permisos suficientes "
            "para realizar esta acción.\n"
            f"🔐 Necesito: `{permisos}`"
        )

        return

    if isinstance(
        original,
        commands.MissingRequiredArgument
    ):

        comando = (
            ctx.command.name
            if ctx.command
            else "este comando"
        )

        await enviar_seguro(
            ctx,
            f"❌ Faltan argumentos para `{comando}`.\n"
            "📖 Usa `!ayuda` para consultar el uso."
        )

        return

    if isinstance(
        original,
        commands.TooManyArguments
    ):

        await enviar_seguro(
            ctx,
            "❌ Has introducido demasiados argumentos."
        )

        return

    if isinstance(
        original,
        commands.BadArgument
    ):

        await enviar_seguro(
            ctx,
            "❌ Uno de los argumentos no es válido."
        )

        return

    if isinstance(
        original,
        commands.CommandOnCooldown
    ):

        segundos = max(
            1,
            int(
                original.retry_after
            )
        )

        await enviar_seguro(
            ctx,
            f"⏳ Espera **{segundos} segundos** "
            "antes de volver a usar este comando."
        )

        return

    if isinstance(
        original,
        commands.NSFWChannelRequired
    ):

        await enviar_seguro(
            ctx,
            "🔞 Este comando requiere un canal NSFW."
        )

        return

    if isinstance(
        original,
        commands.NoPrivateMessage
    ):

        await enviar_seguro(
            ctx,
            "❌ Este comando no puede utilizarse "
            "por mensaje privado."
        )

        return

    if isinstance(
        original,
        commands.PrivateMessageOnly
    ):

        await enviar_seguro(
            ctx,
            "❌ Este comando solo puede utilizarse "
            "por mensaje privado."
        )

        return

    comando = (
        ctx.command.name
        if ctx.command
        else "desconocido"
    )

    logger.error(
        "=================================================="
    )

    logger.error(
        "❌ ERROR EN COMANDO: !%s",
        comando
    )

    logger.error(
        "Usuario: %s (%s)",
        ctx.author,
        ctx.author.id
    )

    logger.error(
        "Servidor: %s",
        getattr(
            ctx.guild,
            "name",
            "DM"
        )
    )

    logger.error(
        "Error: %s",
        original
    )

    logger.error(
        "=================================================="
    )

    traceback.print_exc()

    await enviar_seguro(
        ctx,
        "❌ Ha ocurrido un error inesperado "
        "al ejecutar el comando.\n"
        "🦊 Foxy ha registrado el error."
    )


# ============================================================
# 56. MANEJADOR DE ERRORES DE EVENTOS
# ============================================================

@bot.event
async def on_error(
    event_method,
    *args,
    **kwargs
):

    estadisticas_bot[
        "errores"
    ] += 1

    logger.error(
        "❌ Error en evento: %s",
        event_method
    )

    traceback.print_exc()


# ============================================================
# 57. DESCONEXIÓN
# ============================================================

@bot.event
async def on_disconnect():

    logger.warning(
        "⚠️ Foxy se ha desconectado de Discord."
    )


# ============================================================
# 58. CIERRE LIMPIO
# ============================================================

async def cierre_limpio():

    logger.info(
        "🛑 Cerrando DC_Foxy_Bot..."
    )

    if not bot.is_closed():

        try:

            await bot.close()

        except Exception as error:

            logger.error(
                "Error cerrando bot: %s",
                error
            )


# ============================================================
# 59. COMPROBAR TOKEN / MODO DISCORD
# ============================================================

TOKEN = os.getenv(
    "DISCORD_TOKEN",
    ""
).strip()

DISCORD_ACTIVO = bool(
    TOKEN
)

if DISCORD_ACTIVO:

    logger.info(
        "🟢 Discord: ACTIVO"
    )

else:

    logger.warning(
        "=================================================="
    )

    logger.warning(
        "⛔ DISCORD DESACTIVADO"
    )

    logger.warning(
        "No se encontró DISCORD_TOKEN."
    )

    logger.warning(
        "Foxy continuará en modo inactivo."
    )

    logger.warning(
        "Para activar Discord posteriormente:"
    )

    logger.warning(
        "DISCORD_TOKEN=TU_TOKEN"
    )

    logger.warning(
        "=================================================="
    )


# ============================================================
# 60. DIAGNÓSTICO DE DUPLICADOS FINAL
# ============================================================

def diagnostico_comandos():
    """
    Revisa todos los comandos registrados y detecta
    posibles colisiones entre nombres y aliases.
    """

    mapa = {}

    conflictos = []

    for command in bot.commands:

        nombres = nombres_de_comando(
            command
        )

        for nombre in nombres:

            if nombre in mapa:

                conflictos.append(
                    (
                        nombre,
                        mapa[nombre],
                        command.name
                    )
                )

            else:

                mapa[nombre] = command.name

    if conflictos:

        logger.warning(
            "⚠️ Se detectaron %s conflictos de comandos.",
            len(conflictos)
        )

        for (
            nombre,
            anterior,
            nuevo
        ) in conflictos:

            logger.warning(
                "   !%s -> %s / %s",
                nombre,
                anterior,
                nuevo
            )

    else:

        logger.info(
            "✅ Diagnóstico de comandos: "
            "sin duplicados."
        )

    return conflictos


diagnostico_comandos()


# ============================================================
# 61. INFORMACIÓN FINAL DE ARRANQUE
# ============================================================

logger.info(
    "=================================================="
)

logger.info(
    "🦊 DC_FOXY_BOT PREPARADO"
)

logger.info(
    "📦 Versión: %s",
    BOT_VERSION
)

logger.info(
    "⌨️ Prefijo: %s",
    PREFIX
)

logger.info(
    "📜 Comandos: %s",
    len(bot.commands)
)

logger.info(
    "⚙️ Módulos: %s",
    len(sistemas_cargados)
)


# ============================================================
# 🔊 VOICE AUTO
# ============================================================

logger.info(
    "🔊 Voice Auto: %s",
    "ACTIVO" if DISCORD_ACTIVO else "PREPARADO"
)


# ============================================================
# 🟣 TWITCH
# ============================================================

logger.info(
    "🟣 Twitch: %s",
    "ACTIVO" if DISCORD_ACTIVO else "PREPARADO"
)


# ============================================================
# 🤖 OPENAI
# ============================================================

logger.info(
    "🤖 OpenAI: %s",
    "ACTIVO" if DISCORD_ACTIVO else "PREPARADO"
)


logger.info(
    "⏱️ Tiempo de salida automática: 60 segundos"
)

logger.info(
    "🛡️ Protección de comandos duplicados: ACTIVA"
)

logger.info(
    "=================================================="
)


# ============================================================
# 62. ARRANCAR
# ============================================================

if DISCORD_ACTIVO:

    logger.info(
        "🟢 Iniciando conexión con Discord..."
    )

    try:

        bot.run(
            TOKEN
        )

    except KeyboardInterrupt:

        logger.info(
            "🛑 Bot detenido manualmente."
        )

    except discord.LoginFailure:

        logger.critical(
            "❌ TOKEN DE DISCORD INVÁLIDO."
        )

    except discord.PrivilegedIntentsRequired:

        logger.critical(
            "❌ Faltan Intents privilegiados.\n"
            "Activa Message Content Intent y Server Members Intent "
            "en el Developer Portal de Discord."
        )

    except Exception as error:

        logger.critical(
            "❌ ERROR FATAL AL ARRANCAR FOXY:"
        )

        logger.critical(
            "%s",
            error
        )

        traceback.print_exc()

else:

    logger.warning(
        "=================================================="
    )

    logger.warning(
        "⛔ DC_FOXY_BOT NO SE HA INICIADO"
    )

    logger.warning(
        "Discord está desactivado porque no hay DISCORD_TOKEN."
    )

    logger.warning(
        "Todos los módulos permanecen cargados/preparados."
    )

    logger.warning(
        "🟡 Foxy permanecerá ejecutándose en modo inactivo."
    )

    logger.warning(
        "Para detenerlo: CTRL+C"
    )

    logger.warning(
        "Para activar Discord, añade DISCORD_TOKEN al .env."
    )

    logger.warning(
        "=================================================="
    )

    # --------------------------------------------------------
    # MODO INACTIVO
    # --------------------------------------------------------
    #
    # IMPORTANTE:
    # Antes el programa llegaba aquí y terminaba.
    # Ahora se queda ejecutándose sin conectarse a Discord.
    #
    # Discord sigue COMPLETAMENTE DESACTIVADO.
    #
    # --------------------------------------------------------

    try:

        while True:

            time.sleep(3600)

    except KeyboardInterrupt:

        logger.info(
            "🛑 Foxy detenido manualmente."
        )

    except Exception as error:

        logger.critical(
            "❌ Error en modo inactivo: %s",
            error
        )

        traceback.print_exc()
