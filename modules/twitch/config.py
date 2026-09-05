import os

TWITCH_CLIENT_ID = os.getenv("TWITCH_CLIENT_ID", "")
TWITCH_CLIENT_SECRET = os.getenv("TWITCH_CLIENT_SECRET", "")
TWITCH_BROADCASTER_LOGIN = os.getenv("TWITCH_BROADCASTER_LOGIN", "").strip().lower()
TWITCH_BOT_LOGIN = os.getenv("TWITCH_BOT_LOGIN", "").strip().lower()
TWITCH_BOT_ACCESS_TOKEN = os.getenv("TWITCH_BOT_ACCESS_TOKEN", "").strip()
TWITCH_DISCORD_URL = os.getenv("TWITCH_DISCORD_URL", "").strip()
TWITCH_INSTAGRAM_URL = os.getenv("TWITCH_INSTAGRAM_URL", "").strip()

try:
    TWITCH_SOCIAL_INTERVAL = int(
        os.getenv("TWITCH_SOCIAL_INTERVAL", "3600")
    )
except ValueError:
    TWITCH_SOCIAL_INTERVAL = 3600


def twitch_config_ok() -> bool:
    return all([
        TWITCH_CLIENT_ID,
        TWITCH_CLIENT_SECRET,
        TWITCH_BROADCASTER_LOGIN,
    ])


def twitch_config_status() -> dict:
    return {
        "client_id": bool(TWITCH_CLIENT_ID),
        "client_secret": bool(TWITCH_CLIENT_SECRET),
        "broadcaster": bool(TWITCH_BROADCASTER_LOGIN),
        "bot_login": bool(TWITCH_BOT_LOGIN),
        "bot_token": bool(TWITCH_BOT_ACCESS_TOKEN),
        "discord_url": bool(TWITCH_DISCORD_URL),
        "instagram_url": bool(TWITCH_INSTAGRAM_URL),
        "social_interval": TWITCH_SOCIAL_INTERVAL,
    }