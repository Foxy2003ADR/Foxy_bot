import json
import os
import re
import time
from collections import defaultdict, deque

import discord
from discord.ext import commands


CONFIG_FILE = "security_config.json"


# ============================================================
# CONFIGURACIÓN
# ============================================================

DEFAULT_CONFIG = {
    "enabled": True,
    "anti_spam": True,
    "anti_mass_mention": True,
    "anti_invites": True,
    "anti_raid": True,
    "anti_nuke": True,
    "min_account_age_days": 3,
    "spam_messages": 6,
    "spam_seconds": 8,
    "mass_mentions": 5,
    "raid_joins": 6,
    "raid_seconds": 20,
    "nuke_actions": 3,
    "security_channel_id": None,
    "trusted_users": []
}


def load_config():
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f, indent=4)

    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def save_config(config):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)


config = load_config()


def get_guild_config(guild_id):
    guild_id = str(guild_id)

    if guild_id not in config:
        config[guild_id] = DEFAULT_CONFIG.copy()
        save_config(config)

    # Añadir opciones nuevas si actualizamos el bot
    for key, value in DEFAULT_CONFIG.items():
        if key not in config[guild_id]:
            config[guild_id][key] = value

    return config[guild_id]


# ============================================================
# MEMORIA ANTI-SPAM / ANTI-RAID / ANTI-NUKE
# ============================================================

message_history = defaultdict(lambda: defaultdict(deque))
raid_history = defaultdict(deque)
nuke_history = defaultdict(lambda: defaultdict(deque))

invite_regex = re.compile(
    r"(https?://)?(www\.)?(discord\.gg|discord\.com/invite)/[A-Za-z0-9-]+",
    re.IGNORECASE
)


# ============================================================
# UTILIDADES
# ============================================================

def is_trusted(member, guild_config):
    if member.guild.owner_id == member.id:
        return True

    return member.id in guild_config["trusted_users"]


async def security_log(guild, message, color=discord.Color.orange()):
    guild_config = get_guild_config(guild.id)

    channel_id = guild_config.get("security_channel_id")

    if not channel_id:
        return

    channel = guild.get_channel(channel_id)

    if not channel:
        return

    embed = discord.Embed(
        title="🛡️ Foxy Security",
        description=message,
        color=color,
        timestamp=discord.utils.utcnow()
    )

    try:
        await channel.send(embed=embed)
    except discord.HTTPException:
        pass


async def lockdown(guild):
    changed = 0

    for channel in guild.text_channels:
        try:
            overwrite = channel.overwrites_for(guild.default_role)

            if overwrite.send_messages is not False:
                overwrite.send_messages = False
                await channel.set_permissions(
                    guild.default_role,
                    overwrite=overwrite,
                    reason="Foxy Security - Lockdown"
                )
                changed += 1

        except (discord.Forbidden, discord.HTTPException):
            continue

    await security_log(
        guild,
        f"🚨 **LOCKDOWN ACTIVADO**\n"
        f"Se bloquearon aproximadamente **{changed} canales**.",
        discord.Color.red()
    )


async def unlockdown(guild):
    changed = 0

    for channel in guild.text_channels:
        try:
            overwrite = channel.overwrites_for(guild.default_role)

            if overwrite.send_messages is False:
                overwrite.send_messages = None
                await channel.set_permissions(
                    guild.default_role,
                    overwrite=overwrite,
                    reason="Foxy Security - Unlockdown"
                )
                changed += 1

        except (discord.Forbidden, discord.HTTPException):
            continue

    await security_log(
        guild,
        f"🔓 **LOCKDOWN DESACTIVADO**\n"
        f"Se restauraron aproximadamente **{changed} canales**.",
        discord.Color.green()
    )


# ============================================================
# ANTI-SPAM / INVITES / MENCIONES
# ============================================================

async def security_on_message(message):
    if message.author.bot or not message.guild:
        return

    guild = message.guild
    member = message.author
    guild_config = get_guild_config(guild.id)

    if not guild_config["enabled"]:
        return

    if is_trusted(member, guild_config):
        return

    now = time.monotonic()

    # --------------------------------------------------------
    # CUENTA DEMASIADO NUEVA
    # --------------------------------------------------------

    account_age = (
        discord.utils.utcnow() - member.created_at
    ).total_seconds() / 86400

    if account_age < guild_config["min_account_age_days"]:
        await security_log(
            guild,
            f"⚠️ Cuenta nueva detectada: {member.mention}\n"
            f"Antigüedad aproximada: **{account_age:.1f} días**."
        )

    # --------------------------------------------------------
    # ANTI-MASS-MENTION
    # --------------------------------------------------------

    if guild_config["anti_mass_mention"]:
        mention_count = len(message.mentions)

        if mention_count >= guild_config["mass_mentions"]:
            try:
                await message.delete()
            except discord.HTTPException:
                pass

            await security_log(
                guild,
                f"🚨 **Mass Mention detectado**\n"
                f"Usuario: {member.mention}\n"
                f"Menciones: **{mention_count}**",
                discord.Color.red()
            )

            try:
                await member.timeout(
                    discord.utils.utcnow()
                    + __import__("datetime").timedelta(minutes=5),
                    reason="Foxy Security - Mass Mention"
                )
            except (discord.Forbidden, discord.HTTPException):
                pass

            return

    # --------------------------------------------------------
    # ANTI-INVITES
    # --------------------------------------------------------

    if guild_config["anti_invites"]:
        if invite_regex.search(message.content):
            try:
                await message.delete()
            except discord.HTTPException:
                pass

            await security_log(
                guild,
                f"🔗 Invitación de Discord eliminada.\n"
                f"Usuario: {member.mention}",
                discord.Color.orange()
            )

            return

    # --------------------------------------------------------
    # ANTI-SPAM
    # --------------------------------------------------------

    if guild_config["anti_spam"]:
        history = message_history[guild.id][member.id]

        history.append(now)

        while history and now - history[0] > guild_config["spam_seconds"]:
            history.popleft()

        if len(history) >= guild_config["spam_messages"]:
            try:
                await member.timeout(
                    discord.utils.utcnow()
                    + __import__("datetime").timedelta(minutes=2),
                    reason="Foxy Security - Spam"
                )
            except (discord.Forbidden, discord.HTTPException):
                pass

            await security_log(
                guild,
                f"🚨 **Spam detectado**\n"
                f"Usuario: {member.mention}\n"
                f"Mensajes recientes: **{len(history)}**",
                discord.Color.red()
            )

            history.clear()


# ============================================================
# ANTI-RAID
# ============================================================

async def security_on_member_join(member):
    guild = member.guild
    guild_config = get_guild_config(guild.id)

    if not guild_config["enabled"]:
        return

    now = time.monotonic()

    joins = raid_history[guild.id]
    joins.append(now)

    while joins and now - joins[0] > guild_config["raid_seconds"]:
        joins.popleft()

    if len(joins) >= guild_config["raid_joins"]:
        await security_log(
            guild,
            f"🚨 **POSIBLE RAID DETECTADO**\n"
            f"Se detectaron **{len(joins)} entradas** en "
            f"{guild_config['raid_seconds']} segundos.",
            discord.Color.red()
        )

        await lockdown(guild)

        joins.clear()


# ============================================================
# ANTI-NUKE
# ============================================================

async def get_audit_executor(guild, action):
    try:
        async for entry in guild.audit_logs(
            limit=1,
            action=action
        ):
            return entry.user
    except (discord.Forbidden, discord.HTTPException):
        return None

    return None


async def check_nuke(guild, executor, action_name):
    if not executor:
        return

    guild_config = get_guild_config(guild.id)

    if not guild_config["anti_nuke"]:
        return

    if is_trusted(executor, guild_config):
        return

    now = time.monotonic()

    history = nuke_history[guild.id][executor.id]
    history.append(now)

    while history and now - history[0] > 30:
        history.popleft()

    await security_log(
        guild,
        f"⚠️ Acción administrativa sospechosa.\n"
        f"Usuario: {executor.mention}\n"
        f"Acción: **{action_name}**\n"
        f"Acciones recientes: **{len(history)}**"
    )

    if len(history) >= guild_config["nuke_actions"]:
        await security_log(
            guild,
            f"🚨 **POSIBLE ANTI-NUKE ACTIVADO**\n"
            f"Usuario sospechoso: {executor.mention}\n"
            f"Acciones: **{len(history)}**\n\n"
            f"🔒 Se activará el lockdown como medida preventiva.",
            discord.Color.dark_red()
        )

        await lockdown(guild)

        history.clear()


# ============================================================
# EVENTOS ANTI-NUKE
# ============================================================

async def security_on_guild_channel_delete(channel):
    executor = await get_audit_executor(
        channel.guild,
        discord.AuditLogAction.channel_delete
    )

    await check_nuke(
        channel.guild,
        executor,
        "Eliminar canal"
    )


async def security_on_guild_role_delete(role):
    executor = await get_audit_executor(
        role.guild,
        discord.AuditLogAction.role_delete
    )

    await check_nuke(
        role.guild,
        executor,
        "Eliminar rol"
    )


async def security_on_member_ban(guild, user):
    executor = await get_audit_executor(
        guild,
        discord.AuditLogAction.ban
    )

    await check_nuke(
        guild,
        executor,
        "Banear miembro"
    )


# ============================================================
# COMANDOS
# ============================================================

@commands.command(name="security")
@commands.has_permissions(manage_guild=True)
async def security_command(ctx, estado=None):
    guild_config = get_guild_config(ctx.guild.id)

    if estado:
        estado = estado.lower()

        if estado in ["on", "activar", "enable"]:
            guild_config["enabled"] = True
            save_config(config)

            await ctx.send("🛡️ **Foxy Security activado.**")
            return

        if estado in ["off", "desactivar", "disable"]:
            guild_config["enabled"] = False
            save_config(config)

            await ctx.send("⚠️ **Foxy Security desactivado.**")
            return

    estado_texto = "🟢 ACTIVADO" if guild_config["enabled"] else "🔴 DESACTIVADO"

    await ctx.send(
        f"🛡️ **FOXY SECURITY**\n\n"
        f"Estado: **{estado_texto}**\n"
        f"🚨 Anti-Raid: `{guild_config['anti_raid']}`\n"
        f"💬 Anti-Spam: `{guild_config['anti_spam']}`\n"
        f"📢 Anti-Menciones: `{guild_config['anti_mass_mention']}`\n"
        f"🔗 Anti-Invites: `{guild_config['anti_invites']}`\n"
        f"💣 Anti-Nuke: `{guild_config['anti_nuke']}`"
    )


@commands.command(name="trusted")
@commands.has_permissions(administrator=True)
async def trusted_command(ctx, accion=None, miembro: discord.Member = None):
    guild_config = get_guild_config(ctx.guild.id)

    if accion is None:
        await ctx.send(
            "🛡️ Uso:\n"
            "`!trusted add @usuario`\n"
            "`!trusted remove @usuario`\n"
            "`!trusted list`"
        )
        return

    accion = accion.lower()

    if accion == "list":
        if not guild_config["trusted_users"]:
            await ctx.send("🛡️ No hay usuarios añadidos a la lista de confianza.")
            return

        nombres = []

        for user_id in guild_config["trusted_users"]:
            miembro_obj = ctx.guild.get_member(user_id)

            if miembro_obj:
                nombres.append(f"• {miembro_obj.mention}")

        await ctx.send(
            "🛡️ **Usuarios de confianza:**\n"
            + ("\n".join(nombres) if nombres else "Ninguno visible.")
        )
        return

    if miembro is None:
        await ctx.send("❌ Debes mencionar a un usuario.")
        return

    if accion == "add":
        if miembro.id not in guild_config["trusted_users"]:
            guild_config["trusted_users"].append(miembro.id)
            save_config(config)

        await ctx.send(
            f"🛡️ {miembro.mention} añadido a la lista de confianza."
        )
        return

    if accion == "remove":
        if miembro.id in guild_config["trusted_users"]:
            guild_config["trusted_users"].remove(miembro.id)
            save_config(config)

        await ctx.send(
            f"🛡️ {miembro.mention} eliminado de la lista de confianza."
        )
        return

    await ctx.send("❌ Acción no válida.")


@commands.command(name="securitychannel")
@commands.has_permissions(administrator=True)
async def security_channel_command(ctx, channel: discord.TextChannel = None):
    if channel is None:
        await ctx.send(
            "❌ Uso: `!securitychannel #canal`"
        )
        return

    guild_config = get_guild_config(ctx.guild.id)
    guild_config["security_channel_id"] = channel.id
    save_config(config)

    await ctx.send(
        f"✅ Canal de seguridad configurado: {channel.mention}"
    )


@commands.command(name="lockdown")
@commands.has_permissions(administrator=True)
async def lockdown_command(ctx):
    await lockdown(ctx.guild)

    await ctx.send(
        "🔒 **LOCKDOWN ACTIVADO**\n"
        "Foxy Security ha bloqueado los canales de texto."
    )


@commands.command(name="unlockdown")
@commands.has_permissions(administrator=True)
async def unlockdown_command(ctx):
    await unlockdown(ctx.guild)

    await ctx.send(
        "🔓 **LOCKDOWN DESACTIVADO**\n"
        "Los canales han sido desbloqueados."
    )


# ============================================================
# ERRORES
# ============================================================

async def security_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(
            "❌ Necesitas permisos de **Gestionar servidor**."
        )


async def trusted_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(
            "❌ Necesitas permisos de **Administrador**."
        )


# ============================================================
# INSTALACIÓN DEL SISTEMA
# ============================================================

def setup_security(bot):
    bot.add_listener(security_on_message, "on_message")
    bot.add_listener(security_on_member_join, "on_member_join")
    bot.add_listener(security_on_guild_channel_delete, "on_guild_channel_delete")
    bot.add_listener(security_on_guild_role_delete, "on_guild_role_delete")
    bot.add_listener(security_on_member_ban, "on_member_ban")

    security_command.error = security_command_error
    trusted_command.error = trusted_command_error

    bot.add_command(security_command)
    bot.add_command(trusted_command)
    bot.add_command(security_channel_command)
    bot.add_command(lockdown_command)
    bot.add_command(unlockdown_command)

    print("🛡️ Sistema de seguridad cargado")