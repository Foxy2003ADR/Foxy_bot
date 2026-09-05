import aiohttp

from .auth import get_app_access_token
from .config import TWITCH_CLIENT_ID


TWITCH_API_URL = "https://api.twitch.tv/helix"


async def twitch_request(endpoint, params=None):
    """
    Realiza una petición a la API de Twitch.
    """

    access_token = await get_app_access_token()

    headers = {
        "Client-ID": TWITCH_CLIENT_ID,
        "Authorization": f"Bearer {access_token}",
    }

    url = f"{TWITCH_API_URL}/{endpoint}"

    async with aiohttp.ClientSession() as session:
        async with session.get(
            url,
            headers=headers,
            params=params
        ) as response:

            data = await response.json()

            if response.status != 200:
                raise RuntimeError(
                    f"Error de Twitch API: {data}"
                )

            return data