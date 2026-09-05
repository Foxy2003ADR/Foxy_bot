import aiohttp

from .config import (
    TWITCH_CLIENT_ID,
    TWITCH_CLIENT_SECRET,
)


TWITCH_TOKEN_URL = "https://id.twitch.tv/oauth2/token"


async def get_app_access_token():
    """
    Obtiene un App Access Token de Twitch.
    """

    if not TWITCH_CLIENT_ID or not TWITCH_CLIENT_SECRET:
        raise RuntimeError(
            "Faltan TWITCH_CLIENT_ID o TWITCH_CLIENT_SECRET."
        )

    params = {
        "client_id": TWITCH_CLIENT_ID,
        "client_secret": TWITCH_CLIENT_SECRET,
        "grant_type": "client_credentials",
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(
            TWITCH_TOKEN_URL,
            params=params
        ) as response:

            data = await response.json()

            if response.status != 200:
                raise RuntimeError(
                    f"Error autenticando con Twitch: {data}"
                )

            return data["access_token"]