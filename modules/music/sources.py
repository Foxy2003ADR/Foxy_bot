import asyncio
import re

import yt_dlp

from .queue import Song


YTDLP_OPTIONS = {
    "format": "bestaudio/best",
    "quiet": True,
    "no_warnings": True,
    "noplaylist": True,
    "extract_flat": False,
}


def _extract_info(query: str):
    options = YTDLP_OPTIONS.copy()

    if not query.startswith(("http://", "https://")):
        query = f"ytsearch1:{query}"

    with yt_dlp.YoutubeDL(options) as ydl:
        return ydl.extract_info(query, download=False)


async def search_youtube(
    query: str,
    requester: str | None = None
) -> Song:

    loop = asyncio.get_running_loop()

    info = await loop.run_in_executor(
        None,
        lambda: _extract_info(query)
    )

    if not info:
        raise ValueError("No encontré ninguna canción.")

    if "entries" in info:
        entries = info.get("entries") or []

        if not entries:
            raise ValueError("No encontré ninguna canción.")

        info = entries[0]

    title = info.get("title", "Canción desconocida")
    webpage_url = info.get("webpage_url") or info.get("original_url")

    if not webpage_url:
        raise ValueError("No pude obtener el enlace de la canción.")

    return Song(
        title=title,
        url=webpage_url,
        webpage_url=webpage_url,
        duration=info.get("duration"),
        requester=requester,
    )


async def get_audio_url(webpage_url: str) -> str:

    loop = asyncio.get_running_loop()

    def extract():
        options = {
            "format": "bestaudio/best",
            "quiet": True,
            "no_warnings": True,
            "noplaylist": True,
        }

        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(
                webpage_url,
                download=False
            )

            if not info:
                raise ValueError("No pude obtener el audio.")

            return info["url"]

    return await loop.run_in_executor(None, extract)


def is_youtube_url(value: str) -> bool:
    pattern = r"(youtube\.com|youtu\.be)"
    return bool(re.search(pattern, value, re.IGNORECASE))