import discord
from discord.ext import commands


CONFIG_FILE = "security_config.json"


def get_config():
    import json
    import os

    if not os.path.exists(CONFIG_FILE):
        return {}

    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_config(config):
    import json

    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)


async def send_log(guild, title, description, color=discord.Color.blue()):
    config = get_config()
    guild_config = config.get(str(guild.id), {})

    channel_id = guild_config.get("log_channel_id")

    if not channel_id:
        return

    channel = guild.get_channel(channel_id)

    if not channel:
        return

    embed = discord.Embed(
        title=title,
        description=description,
        color=color,
        timestamp=discord.utils.utcnow()
    )

    try:
        await channel.send(embed=embed)
    except (discord.Forbidden, discord.HTTPException):
        pass


# ============================================================
# CONFIGURAR CANAL DE LOGS
# ============================================================

@commands.command(name="logchannel")
@commands.has_permissions(administrator=True)
async def logchannel(ctx, channel: discord.TextChannel = None):

    if channel is None:
        await ctx.send(
            "❌ Uso correcto: `!logchannel #canal`"
        )
        return

    config = get_config()
    guild_id = str(ctx.guild.id)

    if guild_id not in config:
        config[guild_id] = {}

    config[guild_id]["log_channel_id"] = channel.id

    save_config(config)

    await ctx.send(
        f"📋 Canal de logs configurado correctamente: {channel.mention}"
    )


# ============================================================
# MENSAJE ELIMINADO
# ============================================================

async def on_message_delete(message):

    if not message.guild:
        return

    if message.author.bot:
        return

    contenido = message.content

    if not contenido:
        contenido = "*Sin contenido de texto*"

    if len(contenido) > 1000:
        contenido = contenido[:1000] + "..."

    await send_log(
        message.guild,
        "🗑️ Mensaje eliminado",
        f"👤 Usuario: {message.author.mention}\n"
        f"📍 Canal: {message.channel.mention}\n\n"
        f"💬 Contenido:\n```{contenido}```",
        discord.Color.red()
    )


# ============================================================
# MENSAJE EDITADO
# ============================================================

async def on_message_edit(before, after):

    if not before.guild:
        return

    if before.author.bot:
        return

    if before.content == after.content:
        return

    antiguo = before.content or "*Sin contenido*"
    nuevo = after.content or "*Sin contenido*"

    if len(antiguo) > 700:
        antiguo = antiguo[:700] + "..."

    if len(nuevo) > 700:
        nuevo = nuevo[:700] + "..."

    await send_log(
        before.guild,
        "✏️ Mensaje editado",
        f"👤 Usuario: {before.author.mention}\n"
        f"📍 Canal: {before.channel.mention}\n\n"
        f"🔴 Antes:\n```{antiguo}```\n"
        f"🟢 Después:\n```{nuevo}```",
        discord.Color.orange()
    )


# ============================================================
# MIEMBRO ENTRA
# ============================================================

async def on_member_join(member):

    await send_log(
        member.guild,
        "👋 Miembro entró",
        f"👤 Usuario: {member.mention}\n"
        f"🆔 ID: `{member.id}`\n"
        f"📅 Cuenta creada: <t:{int(member.created_at.timestamp())}:R>",
        discord.Color.green()
    )


# ============================================================
# MIEMBRO SALE
# ============================================================

async def on_member_remove(member):

    await send_log(
        member.guild,
        "🚪 Miembro salió",
        f"👤 Usuario: **{member.name}**\n"
        f"🆔 ID: `{member.id}`",
        discord.Color.orange()
    )


# ============================================================
# ROL CREADO
# ============================================================

async def on_guild_role_create(role):

    await send_log(
        role.guild,
        "🎭 Rol creado",
        f"🎭 Rol: {role.mention}\n"
        f"🆔 ID: `{role.id}`",
        discord.Color.green()
    )


# ============================================================
# ROL ELIMINADO
# ============================================================

async def on_guild_role_delete(role):

    await send_log(
        role.guild,
        "🗑️ Rol eliminado",
        f"🎭 Rol: **{role.name}**\n"
        f"🆔 ID: `{role.id}`",
        discord.Color.red()
    )


# ============================================================
# CANAL CREADO
# ============================================================

async def on_guild_channel_create(channel):

    await send_log(
        channel.guild,
        "📁 Canal creado",
        f"📌 Canal: {channel.mention}\n"
        f"🆔 ID: `{channel.id}`",
        discord.Color.green()
    )


# ============================================================
# CANAL ELIMINADO
# ============================================================

async def on_guild_channel_delete(channel):

    await send_log(
        channel.guild,
        "🗑️ Canal eliminado",
        f"📁 Canal: **{channel.name}**\n"
        f"🆔 ID: `{channel.id}`",
        discord.Color.red()
    )


# ============================================================
# INSTALAR LOGS
# ============================================================

def setup_logs(bot):

    bot.add_command(logchannel)

    bot.add_listener(on_message_delete, "on_message_delete")
    bot.add_listener(on_message_edit, "on_message_edit")
    bot.add_listener(on_member_join, "on_member_join")
    bot.add_listener(on_member_remove, "on_member_remove")
    bot.add_listener(on_guild_role_create, "on_guild_role_create")
    bot.add_listener(on_guild_role_delete, "on_guild_role_delete")
    bot.add_listener(on_guild_channel_create, "on_guild_channel_create")
    bot.add_listener(on_guild_channel_delete, "on_guild_channel_delete")

    print("📋 Sistema de logs cargado")