import logging


logger = logging.getLogger("DC_Foxy_Bot")


# ============================================================
# 🟣 TWITCH MODERATION
# ============================================================

class TwitchModeration:
    """
    Gestiona la configuración de moderación de Twitch.
    """

    def __init__(self):
        self.active = False

    async def start(self):
        """
        Activa el sistema de moderación.
        """

        self.active = True

        logger.info(
            "🛡️ Twitch Moderation preparado."
        )

    async def stop(self):
        """
        Detiene el sistema de moderación.
        """

        self.active = False

        logger.info(
            "🛡️ Twitch Moderation detenido."
        )

    def is_active(self):
        """
        Comprueba si la moderación está activa.
        """

        return self.active


# Instancia global del sistema
twitch_moderation = TwitchModeration()