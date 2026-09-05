# modules/foxy_player.py

"""
🦊 Foxy Player
Jugador virtual de Foxy para el sistema de búsqueda de partidas.

Este módulo NO modifica Discord ni registra comandos.
Solo proporciona la información y funciones necesarias
para tratar a Foxy como jugador virtual.
"""

FOXY_ID = "foxy_virtual"
FOXY_NOMBRE = "Foxy"


def crear_foxy():
    """
    Crea la representación de Foxy como jugador virtual.
    """
    return {
        "id": FOXY_ID,
        "nombre": FOXY_NOMBRE,
        "virtual": True,
    }


def es_foxy(jugador):
    """
    Comprueba si un jugador es Foxy.
    """
    if isinstance(jugador, dict):
        return jugador.get("id") == FOXY_ID

    return False


def nombre_jugador(jugador):
    """
    Devuelve el nombre que debe mostrarse para un jugador.
    """
    if es_foxy(jugador):
        return "🦊 Foxy"

    # Jugador normal de Discord
    if hasattr(jugador, "display_name"):
        return jugador.display_name

    if hasattr(jugador, "name"):
        return jugador.name

    return str(jugador)


def mencion_jugador(jugador):
    """
    Devuelve cómo mostrar al jugador en Discord.
    """
    if es_foxy(jugador):
        return "🦊 Foxy"

    # Jugador normal de Discord
    if hasattr(jugador, "mention"):
        return jugador.mention

    return nombre_jugador(jugador)


def foxy_puede_unirse(jugadores, max_jugadores=5):
    """
    Comprueba si Foxy puede entrar en la partida.
    """
    if len(jugadores) >= max_jugadores:
        return False

    if any(es_foxy(jugador) for jugador in jugadores):
        return False

    return True