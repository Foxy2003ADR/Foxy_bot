# ============================================================
# 🟣 DC_FOXY_BOT — TWITCH MODULE
# ============================================================

from .commands import setup_twitch as setup_twitch_commands
from .chat import start_twitch_chat


def setup_twitch(bot):
    """
    Inicializa el módulo completo de Twitch.

    Incluye:
    - Comandos de Twitch para Discord
    - Chat de Twitch
    - Arranque automático del chat al conectar Discord
    """

    # --------------------------------------------------------
    # COMANDOS DE DISCORD
    # --------------------------------------------------------

    setup_twitch_commands(bot)

    # --------------------------------------------------------
    # CHAT DE TWITCH
    # --------------------------------------------------------

    @bot.listen("on_ready")
    async def _start_twitch_chat():

        try:

            start_twitch_chat()

        except Exception as error:

            print(
                f"[TWITCH] Error iniciando el chat: {error}"
            )