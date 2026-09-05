import logging

import discord


logger = logging.getLogger("DC_Foxy_Bot")


# ============================================================
# 🟣 TWITCH → DISCORD ALERTS
# ============================================================

async def send_twitch_alert(
    bot,
    channel_id: int,
    title: str,
    description: str
):
    """
    Envía una alerta de Twitch a un canal de Discord.
    """

    channel = bot.get_channel(channel_id)

    if channel is None:
        logger.warning(
            "No se encontró el canal de Discord %s.",
            channel_id
        )
        return False

    embed = discord.Embed(
        title=title,
        description=description,
        color=discord.Color.purple()
    )

    embed.set_footer(
        text="🟣 Twitch • DC_Foxy_Bot"
    )

    try:
        await channel.send(embed=embed)
        return True

    except discord.DiscordException as error:
        logger.error(
            "Error enviando alerta de Twitch: %s",
            error
        )
        return False