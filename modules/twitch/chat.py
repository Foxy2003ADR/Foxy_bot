# ============================================================
# 🟣 DC_FOXY_BOT — TWITCH CHAT
# ============================================================
#
# Funciones:
# - Conexión al chat de Twitch mediante IRC/WebSocket
# - Lectura de mensajes
# - Detección de comandos
# - Reconexión automática
# - Identificación básica de usuarios
# - Comandos básicos de Twitch
#
# ============================================================

import asyncio
import logging
from datetime import datetime, timezone

import aiohttp

from .config import (
    TWITCH_CLIENT_ID,
    TWITCH_BOT_ACCESS_TOKEN,
    TWITCH_BOT_LOGIN,
    TWITCH_BROADCASTER_LOGIN,
)

from .streams import (
    get_stream,
    get_channel,
)

logger = logging.getLogger("DC_Foxy_Bot")


# ============================================================
# CONFIGURACIÓN
# ============================================================

TWITCH_CHAT_URL = (
    "https://api.twitch.tv/helix/chat/messages"
)

TWITCH_USERS_URL = (
    "https://api.twitch.tv/helix/users"
)

TWITCH_IRC_HOST = "irc-ws.chat.twitch.tv"
TWITCH_IRC_PORT = 443

TWITCH_CHANNEL = (
    TWITCH_BROADCASTER_LOGIN
    or "foxy2003_"
).strip().lower()


# ============================================================
# UTILIDADES DE TOKEN
# ============================================================

def _clean_token(token: str) -> str:
    """
    Limpia un token de Twitch.

    Acepta:
        oauth:xxxxxxxx

    o:
        xxxxxxxx
    """

    token = (token or "").strip()

    if token.lower().startswith("oauth:"):
        token = token[6:]

    return token


def _irc_token(token: str) -> str:
    """
    Prepara el token para IRC.
    """

    return f"oauth:{_clean_token(token)}"


# ============================================================
# OBTENER ID DEL BOT
# ============================================================

async def get_bot_user_id() -> str:
    """
    Obtiene el ID numérico del usuario del bot.
    """

    if not TWITCH_CLIENT_ID:
        raise RuntimeError(
            "Falta TWITCH_CLIENT_ID."
        )

    if not TWITCH_BOT_LOGIN:
        raise RuntimeError(
            "Falta TWITCH_BOT_LOGIN."
        )

    token = _clean_token(
        TWITCH_BOT_ACCESS_TOKEN
    )

    if not token:
        raise RuntimeError(
            "Falta TWITCH_BOT_ACCESS_TOKEN."
        )

    headers = {
        "Client-Id": TWITCH_CLIENT_ID,
        "Authorization": f"Bearer {token}",
    }

    params = {
        "login": TWITCH_BOT_LOGIN,
    }

    timeout = aiohttp.ClientTimeout(
        total=15
    )

    async with aiohttp.ClientSession(
        timeout=timeout
    ) as session:

        async with session.get(
            TWITCH_USERS_URL,
            headers=headers,
            params=params,
        ) as response:

            try:
                data = await response.json()
            except Exception:
                data = {}

            if response.status != 200:
                raise RuntimeError(
                    "Error obteniendo el usuario "
                    f"del bot ({response.status}): {data}"
                )

            users = data.get(
                "data",
                []
            )

            if not users:
                raise RuntimeError(
                    "No se encontró el usuario "
                    f"de Twitch '{TWITCH_BOT_LOGIN}'."
                )

            user_id = users[0].get("id")

            if not user_id:
                raise RuntimeError(
                    "Twitch no devolvió "
                    "el ID del bot."
                )

            return str(user_id)


# ============================================================
# ENVIAR MENSAJE AL CHAT MEDIANTE API
# ============================================================

async def send_chat_message(
    broadcaster_id: str,
    message: str,
) -> bool:
    """
    Envía un mensaje al chat mediante
    la API oficial de Twitch.
    """

    if not TWITCH_CLIENT_ID:
        raise RuntimeError(
            "Falta TWITCH_CLIENT_ID."
        )

    if not TWITCH_BOT_ACCESS_TOKEN:
        raise RuntimeError(
            "Falta TWITCH_BOT_ACCESS_TOKEN."
        )

    if not TWITCH_BOT_LOGIN:
        raise RuntimeError(
            "Falta TWITCH_BOT_LOGIN."
        )

    if not broadcaster_id:
        raise ValueError(
            "Falta broadcaster_id."
        )

    message = str(
        message or ""
    ).strip()

    if not message:
        return False

    message = message[:500]

    token = _clean_token(
        TWITCH_BOT_ACCESS_TOKEN
    )

    bot_user_id = await get_bot_user_id()

    headers = {
        "Client-Id": TWITCH_CLIENT_ID,
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    payload = {
        "broadcaster_id": str(
            broadcaster_id
        ),
        "sender_id": str(
            bot_user_id
        ),
        "message": message,
    }

    timeout = aiohttp.ClientTimeout(
        total=15
    )

    async with aiohttp.ClientSession(
        timeout=timeout
    ) as session:

        async with session.post(
            TWITCH_CHAT_URL,
            headers=headers,
            json=payload,
        ) as response:

            try:
                data = await response.json()
            except Exception:
                data = {}

            if response.status not in (
                200,
                202,
            ):
                logger.error(
                    "Error enviando mensaje "
                    "a Twitch (%s): %s",
                    response.status,
                    data,
                )
                return False

            logger.debug(
                "Mensaje enviado a Twitch: %s",
                message,
            )

            return True


async def send_chat_message_safe(
    broadcaster_id: str,
    message: str,
) -> bool:
    """
    Versión segura de send_chat_message().
    """

    try:
        return await send_chat_message(
            broadcaster_id=broadcaster_id,
            message=message,
        )

    except Exception as error:

        logger.error(
            "No se pudo enviar mensaje "
            "a Twitch: %s",
            error,
            exc_info=True,
        )

        return False


# ============================================================
# PARSER IRC
# ============================================================

def parse_irc_message(
    raw_message: str,
) -> dict:
    """
    Analiza una línea IRC de Twitch.
    """

    result = {
        "raw": raw_message,
        "tags": {},
        "prefix": "",
        "command": "",
        "params": [],
        "username": "",
        "message": "",
    }

    line = raw_message.rstrip(
        "\r\n"
    )

    if not line:
        return result

    # --------------------------------------------------------
    # TAGS
    # --------------------------------------------------------

    if line.startswith("@"):

        try:
            tags_part, line = line.split(
                " ",
                1
            )

        except ValueError:
            return result

        tags_part = tags_part[1:]

        for item in tags_part.split(";"):

            if "=" in item:

                key, value = item.split(
                    "=",
                    1
                )

                result["tags"][key] = value

            else:

                result["tags"][item] = ""

    # --------------------------------------------------------
    # PREFIX
    # --------------------------------------------------------

    if line.startswith(":"):

        try:
            prefix, line = line.split(
                " ",
                1
            )

        except ValueError:
            return result

        result["prefix"] = prefix[1:]

    # --------------------------------------------------------
    # MENSAJE
    # --------------------------------------------------------

    if " :" in line:

        before, message = line.split(
            " :",
            1
        )

        result["message"] = message

    else:

        before = line

    parts = before.split()

    if not parts:
        return result

    result["command"] = parts[0].upper()

    result["params"] = parts[1:]

    # --------------------------------------------------------
    # USUARIO
    # --------------------------------------------------------

    username = result["tags"].get(
        "display-name"
    )

    if not username:

        username = result["tags"].get(
            "login"
        )

    if not username and result["prefix"]:

        username = result["prefix"].split(
            "!",
            1
        )[0]

    result["username"] = (
        username or ""
    )

    return result


# ============================================================
# PERMISOS
# ============================================================

def get_user_permissions(
    parsed: dict,
) -> dict:
    """
    Obtiene permisos básicos desde
    las tags de Twitch.
    """

    tags = parsed.get(
        "tags",
        {}
    )

    badges = tags.get(
        "badges",
        ""
    )

    badges_lower = badges.lower()

    return {
        "subscriber": (
            "subscriber/" in badges_lower
        ),

        "vip": (
            "vip/" in badges_lower
        ),

        "moderator": (
            "moderator/" in badges_lower
            or tags.get("mod") == "1"
        ),

        "broadcaster": (
            "broadcaster/" in badges_lower
        ),

        "staff": (
            "staff/" in badges_lower
        ),

        "admin": (
            "admin/" in badges_lower
        ),
    }


def is_moderator(
    parsed: dict,
) -> bool:
    """
    Comprueba si el usuario tiene
    permisos elevados.
    """

    permissions = get_user_permissions(
        parsed
    )

    return (
        permissions["moderator"]
        or permissions["broadcaster"]
        or permissions["staff"]
        or permissions["admin"]
    )


# ============================================================
# FORMATEAR UPTIME
# ============================================================

def format_uptime(
    started_at: str,
) -> str:
    """
    Convierte started_at de Twitch
    en un tiempo legible.
    """

    if not started_at:
        return "desconocido"

    try:

        started = datetime.fromisoformat(
            started_at.replace(
                "Z",
                "+00:00"
            )
        )

        now = datetime.now(
            timezone.utc
        )

        elapsed = now - started

        total_seconds = max(
            0,
            int(
                elapsed.total_seconds()
            )
        )

        hours, remainder = divmod(
            total_seconds,
            3600
        )

        minutes, seconds = divmod(
            remainder,
            60
        )

        if hours:
            return (
                f"{hours}h "
                f"{minutes}m"
            )

        if minutes:
            return (
                f"{minutes}m "
                f"{seconds}s"
            )

        return f"{seconds}s"

    except Exception:

        return "desconocido"


# ============================================================
# COMANDOS DEL CHAT
# ============================================================

async def handle_chat_command(
    chat,
    parsed: dict,
) -> None:
    """
    Procesa comandos enviados en Twitch.
    """

    message = (
        parsed.get(
            "message",
            ""
        )
        .strip()
    )

    if not message.startswith("!"):
        return

    parts = message.split()

    command = (
        parts[0][1:]
        .lower()
    )

    args = parts[1:]

    username = (
        parsed.get(
            "username"
        )
        or "usuario"
    )

    # ========================================================
    # !HOLA
    # ========================================================

    if command == "hola":

        await chat.send(
            f"👋 ¡Hola, {username}! "
            "Bienvenido al directo de Foxy 🦊"
        )

        return

    # ========================================================
    # !DISCORD
    # ========================================================

    if command == "discord":

        await chat.send(
            "💬 Discord de Foxy: "
            "https://discord.gg/ZJzJnztn5r"
        )

        return

    # ========================================================
    # !INSTAGRAM
    # ========================================================

    if command == "instagram":

        await chat.send(
            "📸 Instagram de Foxy: "
            "https://www.instagram.com/_foxy2003_/"
        )

        return

    # ========================================================
    # !SOCIALS / !REDES
    # ========================================================

    if command in (
        "socials",
        "redes",
    ):

        await chat.send(
            "🌐 Twitch: "
            "https://www.twitch.tv/foxy2003_ "
            "| 💬 Discord: "
            "https://discord.gg/ZJzJnztn5r "
            "| 📸 Instagram: "
            "https://www.instagram.com/_foxy2003_/"
        )

        return

    # ========================================================
    # !ID
    # ========================================================

    if command == "id":

        user_id = parsed.get(
            "tags",
            {}
        ).get(
            "user-id"
        )

        if user_id:

            await chat.send(
                f"🆔 {username}, "
                f"tu ID de Twitch es {user_id}"
            )

        else:

            await chat.send(
                f"🆔 No pude obtener "
                f"el ID de {username}."
            )

        return

    # ========================================================
    # !COMANDOS
    # ========================================================

    if command in (
        "comandos",
        "commands",
    ):

        await chat.send(
            "📜 Comandos: "
            "!hola !discord !instagram !socials "
            "!id !puntos !uptime !titulo "
            "!categoria !viewers !seguidores "
            "!game !title !stats"
        )

        return

    # ========================================================
    # !UPTIME
    # ========================================================

    if command == "uptime":

        try:

            stream = await get_stream(
                TWITCH_BROADCASTER_LOGIN
            )

            if not stream:

                await chat.send(
                    "⚫ Foxy no está "
                    "en directo ahora mismo."
                )

                return

            uptime = format_uptime(
                stream.get(
                    "started_at",
                    ""
                )
            )

            await chat.send(
                f"🔴 Foxy lleva "
                f"{uptime} en directo."
            )

        except Exception as error:

            logger.error(
                "Error en !uptime: %s",
                error,
                exc_info=True,
            )

            await chat.send(
                "⚠️ No pude obtener el uptime."
            )

        return

    # ========================================================
    # !VIEWERS
    # ========================================================

    if command in (
        "viewers",
        "espectadores",
    ):

        try:

            stream = await get_stream(
                TWITCH_BROADCASTER_LOGIN
            )

            if not stream:

                await chat.send(
                    "⚫ El canal está offline."
                )

                return

            viewers = stream.get(
                "viewer_count",
                0
            )

            await chat.send(
                f"👀 Ahora mismo hay "
                f"{viewers} espectadores."
            )

        except Exception as error:

            logger.error(
                "Error en !viewers: %s",
                error,
                exc_info=True,
            )

            await chat.send(
                "⚠️ No pude consultar "
                "los espectadores."
            )

        return

    # ========================================================
    # !TITULO / !TITLE
    # ========================================================

    if command in (
        "titulo",
        "title",
    ):

        try:

            channel_data = await get_channel(
                TWITCH_BROADCASTER_LOGIN
            )

            if not channel_data:

                await chat.send(
                    "⚠️ No pude obtener "
                    "el título actual."
                )

                return

            title = channel_data.get(
                "title",
                "Sin título"
            )

            await chat.send(
                f"📝 Título actual: {title}"
            )

        except Exception as error:

            logger.error(
                "Error en !titulo: %s",
                error,
                exc_info=True,
            )

            await chat.send(
                "⚠️ Error consultando "
                "el título."
            )

        return

    # ========================================================
    # !CATEGORIA / !GAME
    # ========================================================

    if command in (
        "categoria",
        "game",
    ):

        try:

            channel_data = await get_channel(
                TWITCH_BROADCASTER_LOGIN
            )

            if not channel_data:

                await chat.send(
                    "⚠️ No pude obtener "
                    "la categoría actual."
                )

                return

            game = channel_data.get(
                "game_name",
                "Sin categoría"
            )

            await chat.send(
                f"🎮 Categoría actual: {game}"
            )

        except Exception as error:

            logger.error(
                "Error en !categoria: %s",
                error,
                exc_info=True,
            )

            await chat.send(
                "⚠️ Error consultando "
                "la categoría."
            )

        return

    # ========================================================
    # !STATS
    # ========================================================

    if command == "stats":

        try:

            stream = await get_stream(
                TWITCH_BROADCASTER_LOGIN
            )

            channel_data = await get_channel(
                TWITCH_BROADCASTER_LOGIN
            )

            if not channel_data:

                await chat.send(
                    "⚠️ No pude obtener "
                    "las estadísticas."
                )

                return

            title = channel_data.get(
                "title",
                "Sin título"
            )

            game = channel_data.get(
                "game_name",
                "Sin categoría"
            )

            if stream:

                viewers = stream.get(
                    "viewer_count",
                    0
                )

                uptime = format_uptime(
                    stream.get(
                        "started_at",
                        ""
                    )
                )

                await chat.send(
                    f"📊 Foxy está EN DIRECTO | "
                    f"👀 {viewers} viewers | "
                    f"🎮 {game} | "
                    f"🕐 {uptime} | "
                    f"📝 {title}"
                )

            else:

                await chat.send(
                    f"📊 Foxy está OFFLINE | "
                    f"🎮 Última categoría: {game} | "
                    f"📝 Título: {title}"
                )

        except Exception as error:

            logger.error(
                "Error en !stats: %s",
                error,
                exc_info=True,
            )

            await chat.send(
                "⚠️ No pude obtener "
                "las estadísticas."
            )

        return

    # ========================================================
    # !PAUSA
    # ========================================================

    if command == "pausa":

        if not is_moderator(parsed):

            await chat.send(
                f"⛔ {username}, "
                "no tienes permiso para usar !pausa."
            )

            return

        chat.paused = True

        await chat.send(
            "⏸️ Automatizaciones de Twitch pausadas."
        )

        return

    # ========================================================
    # !REANUDAR
    # ========================================================

    if command == "reanudar":

        if not is_moderator(parsed):

            await chat.send(
                f"⛔ {username}, "
                "no tienes permiso para usar !reanudar."
            )

            return

        chat.paused = False

        await chat.send(
            "▶️ Automatizaciones de Twitch reanudadas."
        )

        return

    # ========================================================
    # !PUNTOS
    # ========================================================

    if command == "puntos":

        await chat.send(
            f"🪙 {username}, "
            "el sistema de puntos "
            "todavía está preparando "
            "su base de datos."
        )

        return

    # ========================================================
    # COMANDO DESCONOCIDO
    # ========================================================

    logger.debug(
        "Comando Twitch desconocido: %s",
        command,
    )


# ============================================================
# CLASE TWITCH CHAT
# ============================================================

class TwitchChat:
    """
    Cliente IRC de Twitch.

    Mantiene una conexión persistente
    y se reconecta automáticamente.
    """

    def __init__(
        self,
        channel: str | None = None,
    ):

        self.channel = (
            channel
            or TWITCH_CHANNEL
        ).strip().lower()

        self.websocket = None

        self.running = False

        self.connected = False

        self.paused = False

        self.task = None

        self._stop_event = asyncio.Event()

    # ========================================================
    # SEND
    # ========================================================

    async def send(
        self,
        message: str,
    ) -> bool:

        message = str(
            message or ""
        ).strip()

        if not message:
            return False

        if len(message) > 500:
            message = message[:500]

        if not self.websocket:
            return False

        if not self.connected:
            return False

        try:

            await self.websocket.send(
                f"PRIVMSG #{self.channel} :{message}"
            )

            return True

        except Exception as error:

            logger.error(
                "Error enviando mensaje IRC: %s",
                error,
            )

            return False

    # ========================================================
    # CONNECT
    # ========================================================

    async def connect(self):

        if not TWITCH_BOT_LOGIN:

            raise RuntimeError(
                "Falta TWITCH_BOT_LOGIN."
            )

        if not TWITCH_BOT_ACCESS_TOKEN:

            raise RuntimeError(
                "Falta TWITCH_BOT_ACCESS_TOKEN."
            )

        try:

            import websockets

        except ImportError:

            raise RuntimeError(
                "Falta la dependencia 'websockets'. "
                "Instálala con: pip install websockets"
            )

        token = _irc_token(
            TWITCH_BOT_ACCESS_TOKEN
        )

        logger.info(
            "Conectando al chat de Twitch #%s...",
            self.channel,
        )

        self.websocket = await websockets.connect(
            f"wss://{TWITCH_IRC_HOST}:{TWITCH_IRC_PORT}",
            ping_interval=30,
            ping_timeout=30,
            close_timeout=5,
        )

        # ----------------------------------------------------
        # CAPABILITIES
        # ----------------------------------------------------

        await self.websocket.send(
            "CAP REQ :twitch.tv/tags "
            "twitch.tv/commands "
            "twitch.tv/membership"
        )

        # ----------------------------------------------------
        # AUTH
        # ----------------------------------------------------

        await self.websocket.send(
            f"PASS {token}"
        )

        await self.websocket.send(
            f"NICK {TWITCH_BOT_LOGIN.lower()}"
        )

        await self.websocket.send(
            f"JOIN #{self.channel}"
        )

        self.connected = True

        logger.info(
            "✅ Conectado al chat de Twitch #%s",
            self.channel,
        )

    # ========================================================
    # DISCONNECT
    # ========================================================

    async def disconnect(self):

        self.connected = False

        if self.websocket:

            try:

                await self.websocket.close()

            except Exception:
                pass

            self.websocket = None

        logger.info(
            "Chat de Twitch desconectado."
        )

    # ========================================================
    # PROCESS LINE
    # ========================================================

    async def process_line(
        self,
        raw_line: str,
    ):

        parsed = parse_irc_message(
            raw_line
        )

        command = parsed.get(
            "command",
            ""
        )

        # ----------------------------------------------------
        # PING
        # ----------------------------------------------------

        if command == "PING":

            if self.websocket:

                try:

                    await self.websocket.send(
                        "PONG :tmi.twitch.tv"
                    )

                except Exception:
                    pass

            return

        # ----------------------------------------------------
        # PRIVMSG
        # ----------------------------------------------------

        if command == "PRIVMSG":

            logger.info(
                "[TWITCH] %s: %s",
                parsed.get(
                    "username",
                    "?"
                ),
                parsed.get(
                    "message",
                    ""
                ),
            )

            if not self.paused:

                await handle_chat_command(
                    self,
                    parsed,
                )

            return

        # ----------------------------------------------------
        # NOTICE
        # ----------------------------------------------------

        if command == "NOTICE":

            logger.warning(
                "[TWITCH NOTICE] %s",
                parsed.get(
                    "message",
                    ""
                ),
            )

            return

        # ----------------------------------------------------
        # RECONNECT
        # ----------------------------------------------------

        if command == "RECONNECT":

            logger.warning(
                "Twitch solicita reconexión."
            )

            raise ConnectionError(
                "Twitch solicitó reconexión."
            )

    # ========================================================
    # RUN ONCE
    # ========================================================

    async def run_once(self):

        await self.connect()

        try:

            while self.running:

                raw_line = await self.websocket.recv()

                if raw_line is None:
                    break

                if isinstance(
                    raw_line,
                    bytes
                ):

                    raw_line = raw_line.decode(
                        "utf-8",
                        errors="ignore",
                    )

                for line in str(
                    raw_line
                ).splitlines():

                    await self.process_line(
                        line
                    )

        finally:

            await self.disconnect()

    # ========================================================
    # RUN FOREVER
    # ========================================================

    async def run(self):

        if self.running:
            return

        self.running = True

        self._stop_event.clear()

        logger.info(
            "🟣 Iniciando Twitch Chat..."
        )

        delay = 5

        while self.running:

            try:

                await self.run_once()

                delay = 5

            except asyncio.CancelledError:

                logger.info(
                    "Twitch Chat cancelado."
                )

                break

            except Exception as error:

                logger.error(
                    "Error en Twitch Chat: %s",
                    error,
                    exc_info=True,
                )

                await self.disconnect()

                if not self.running:
                    break

                logger.info(
                    "Reconectando Twitch Chat "
                    "en %s segundos...",
                    delay,
                )

                try:

                    await asyncio.wait_for(
                        self._stop_event.wait(),
                        timeout=delay,
                    )

                except asyncio.TimeoutError:
                    pass

                delay = min(
                    delay * 2,
                    60,
                )

        await self.disconnect()

        logger.info(
            "🛑 Twitch Chat detenido."
        )

    # ========================================================
    # START
    # ========================================================

    def start(self):

        if self.task and not self.task.done():
            return self.task

        self.task = asyncio.create_task(
            self.run(),
            name="twitch-chat",
        )

        return self.task

    # ========================================================
    # STOP
    # ========================================================

    async def stop(self):

        self.running = False

        self._stop_event.set()

        await self.disconnect()

        if self.task:

            current_task = (
                asyncio.current_task()
            )

            if self.task is not current_task:

                try:

                    await self.task

                except asyncio.CancelledError:
                    pass

                except Exception:
                    pass

            self.task = None


# ============================================================
# INSTANCIA GLOBAL
# ============================================================

twitch_chat = TwitchChat()


# ============================================================
# FUNCIONES PÚBLICAS
# ============================================================

def start_twitch_chat():
    return twitch_chat.start()


async def stop_twitch_chat():
    await twitch_chat.stop()


def get_twitch_chat():
    return twitch_chat


# ============================================================
# FIN
# ============================================================