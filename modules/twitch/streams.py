from .api import twitch_request


# ============================================================
# 🟣 TWITCH STREAMS
# ============================================================

async def get_stream(channel_name: str):
    """
    Obtiene información del directo de un canal de Twitch.

    Devuelve None si el canal está offline.
    """

    if not channel_name:
        return None

    data = await twitch_request(
        "streams",
        params={
            "user_login": channel_name.strip().lower()
        }
    )

    streams = data.get("data", [])

    if not streams:
        return None

    return streams[0]


async def get_channel(channel_name: str):
    """
    Obtiene información básica de un canal de Twitch.
    """

    if not channel_name:
        return None

    data = await twitch_request(
        "channels",
        params={
            "broadcaster_login": channel_name.strip().lower()
        }
    )

    channels = data.get("data", [])

    if not channels:
        return None

    return channels[0]


async def get_user(login: str):
    """
    Obtiene información de un usuario de Twitch.
    """

    if not login:
        return None

    data = await twitch_request(
        "users",
        params={
            "login": login.strip().lower()
        }
    )

    users = data.get("data", [])

    if not users:
        return None

    return users[0]


async def get_followers(broadcaster_id: str):
    """
    Obtiene información de seguidores del canal.

    Devuelve el objeto completo de Twitch.
    """

    if not broadcaster_id:
        return None

    return await twitch_request(
        "channels/followers",
        params={
            "broadcaster_id": broadcaster_id
        }
    )


async def get_follower_count(broadcaster_id: str):
    """
    Devuelve el número total de seguidores.
    """

    data = await get_followers(broadcaster_id)

    if not data:
        return 0

    return int(data.get("total", 0))


async def search_game(game_name: str):
    """
    Busca una categoría/juego en Twitch.

    Devuelve el primer resultado.
    """

    if not game_name:
        return None

    data = await twitch_request(
        "games",
        params={
            "name": game_name.strip()
        }
    )

    games = data.get("data", [])

    if not games:
        return None

    return games[0]


async def get_game(game_id: str):
    """
    Obtiene información de una categoría mediante su ID.
    """

    if not game_id:
        return None

    data = await twitch_request(
        "games",
        params={
            "id": game_id
        }
    )

    games = data.get("data", [])

    if not games:
        return None

    return games[0]


def get_uptime(stream: dict):
    """
    Calcula el uptime de un directo.

    Devuelve segundos.
    """

    if not stream:
        return 0

    started_at = stream.get("started_at")

    if not started_at:
        return 0

    from datetime import datetime, timezone

    try:
        started = datetime.fromisoformat(
            started_at.replace("Z", "+00:00")
        )

        now = datetime.now(timezone.utc)

        seconds = int(
            (now - started).total_seconds()
        )

        return max(seconds, 0)

    except Exception:
        return 0