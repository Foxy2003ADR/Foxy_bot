import json
import os


# ============================================================
# 🟣 TWITCH DATABASE
# ============================================================

DATABASE_FILE = "twitch_data.json"


def load_data():
    """
    Carga la configuración guardada de Twitch.
    """

    if not os.path.exists(DATABASE_FILE):
        return {}

    try:
        with open(
            DATABASE_FILE,
            "r",
            encoding="utf-8"
        ) as file:
            return json.load(file)

    except (json.JSONDecodeError, OSError):
        return {}


def save_data(data):
    """
    Guarda la configuración de Twitch.
    """

    with open(
        DATABASE_FILE,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )


def get_guild_config(guild_id: int):
    """
    Obtiene la configuración de un servidor de Discord.
    """

    data = load_data()

    return data.get(
        str(guild_id),
        {}
    )


def set_guild_config(
    guild_id: int,
    config: dict
):
    """
    Guarda la configuración de un servidor.
    """

    data = load_data()

    data[str(guild_id)] = config

    save_data(data)