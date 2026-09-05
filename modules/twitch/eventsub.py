import logging


logger = logging.getLogger("DC_Foxy_Bot")


# ============================================================
# 🟣 TWITCH EVENTSUB
# ============================================================

EVENTSUB_EVENTS = {
    "stream.online": "Directo iniciado",
    "stream.offline": "Directo finalizado",
    "channel.follow": "Nuevo follow",
    "channel.subscribe": "Nueva suscripción",
    "channel.subscription.gift": "Suscripción regalada",
    "channel.cheer": "Bits recibidos",
    "channel.channel_points_custom_reward_redemption.add": (
        "Canje de puntos del canal"
    ),
    "channel.update": "Canal actualizado",
}


class TwitchEventSub:
    """
    Gestiona la configuración de eventos de Twitch.
    """

    def __init__(self):
        self.active = False

    async def start(self):
        """
        Inicia EventSub.
        """
        self.active = True

        logger.info(
            "🟣 Twitch EventSub preparado."
        )

    async def stop(self):
        """
        Detiene EventSub.
        """
        self.active = False

        logger.info(
            "🟣 Twitch EventSub detenido."
        )

    def is_active(self):
        """
        Indica si EventSub está activo.
        """
        return self.active