# modules/shop.py

"""
🛒 Foxy Shop
Tienda de objetos para Foxy.

Utiliza:
- modules/foxy_core.py -> dinero
- modules/inventory.py -> inventario

No crea un sistema de dinero separado.
"""

import discord
from discord.ext import commands

from modules.foxy_core import (
    obtener_foxy,
    añadir_dinero,
    quitar_dinero,
)

from modules.inventory import (
    añadir_objeto,
    obtener_cantidad,
    OBJETOS,
)


# ============================================================
# PRODUCTOS DE LA TIENDA
# ============================================================

TIENDA = {
    "pocion_vida": {
        "precio": 100,
        "nombre": "🧪 Poción de Vida",
        "descripcion": "Restaura 25 puntos de vida.",
    },

    "pocion_energia": {
        "precio": 120,
        "nombre": "⚡ Poción de Energía",
        "descripcion": "Restaura 30 puntos de energía.",
    },

    "comida": {
        "precio": 50,
        "nombre": "🍖 Comida",
        "descripcion": "Restaura vida y energía.",
    },
}


# ============================================================
# FUNCIONES
# ============================================================

def formatear_dinero(cantidad):
    return f"{cantidad:,}".replace(",", ".")


def obtener_dinero():
    foxy = obtener_foxy()
    return foxy.get("dinero", 0)


def comprar_objeto(objeto, cantidad=1):
    """
    Compra un objeto y lo añade al inventario.
    """

    if objeto not in TIENDA:
        return False, "❌ Ese objeto no está disponible en la tienda."

    if cantidad <= 0:
        return False, "❌ La cantidad debe ser mayor que 0."

    producto = TIENDA[objeto]

    precio_total = producto["precio"] * cantidad
    dinero = obtener_dinero()

    if dinero < precio_total:
        return False, (
            "❌ Foxy no tiene suficiente dinero.\n"
            f"💰 Necesita: **{formatear_dinero(precio_total)} monedas**\n"
            f"💳 Tiene: **{formatear_dinero(dinero)} monedas**"
        )

    if not quitar_dinero(precio_total):
        return False, "❌ No se pudo realizar la compra."

    if not añadir_objeto(objeto, cantidad):
        # Devolver el dinero si por algún motivo falla
        añadir_dinero(precio_total)

        return False, "❌ No se pudo añadir el objeto al inventario."

    return True, (
        f"✅ Compra realizada.\n"
        f"{producto['nombre']} ×**{cantidad}**\n"
        f"💰 Precio: **{formatear_dinero(precio_total)} monedas**\n"
        f"💳 Saldo restante: **{formatear_dinero(obtener_dinero())} monedas**"
    )


# ============================================================
# COMANDO: TIENDA
# ============================================================

@commands.command(
    name="tienda",
    aliases=["shop", "store"]
)
async def tienda(ctx):

    embed = discord.Embed(
        title="🛒 Tienda de Foxy",
        description=(
            "Compra objetos para Foxy.\n\n"
            f"💰 Saldo actual: "
            f"**{formatear_dinero(obtener_dinero())} monedas**\n\n"
            "Para comprar:\n"
            "`!comprar objeto cantidad`"
        ),
        color=discord.Color.gold()
    )

    for objeto_id, producto in TIENDA.items():

        cantidad_inventario = obtener_cantidad(objeto_id)

        embed.add_field(
            name=(
                f"{producto['nombre']} — "
                f"💰 {formatear_dinero(producto['precio'])}"
            ),
            value=(
                f"{producto['descripcion']}\n"
                f"🎒 En inventario: **{cantidad_inventario}**\n"
                f"📦 ID: `{objeto_id}`"
            ),
            inline=False
        )

    await ctx.send(embed=embed)


# ============================================================
# COMANDO: COMPRAR
# ============================================================

@commands.command(
    name="comprar",
    aliases=["buy"]
)
async def comprar(ctx, objeto=None, cantidad: int = 1):

    if objeto is None:
        await ctx.send(
            "❌ Debes indicar qué quieres comprar.\n\n"
            "Ejemplo:\n"
            "`!comprar pocion_vida 2`\n\n"
            "Usa `!tienda` para ver los objetos disponibles."
        )
        return

    objeto = objeto.lower().strip()

    # Permitir nombres sencillos
    equivalencias = {
        "pocion": "pocion_vida",
        "poción": "pocion_vida",

        "vida": "pocion_vida",
        "pocion_vida": "pocion_vida",
        "poción_vida": "pocion_vida",

        "energia": "pocion_energia",
        "energía": "pocion_energia",
        "pocion_energia": "pocion_energia",
        "poción_energia": "pocion_energia",
        "poción_energía": "pocion_energia",

        "comida": "comida",
    }

    objeto = equivalencias.get(objeto, objeto)

    correcto, mensaje = comprar_objeto(
        objeto,
        cantidad
    )

    await ctx.send(mensaje)


# ============================================================
# COMANDO: PRECIO
# ============================================================

@commands.command(
    name="precio",
    aliases=["price"]
)
async def precio(ctx, *, objeto=None):

    if objeto is None:
        await ctx.send(
            "❌ Indica el objeto del que quieres saber el precio.\n\n"
            "Ejemplo:\n"
            "`!precio pocion_vida`"
        )
        return

    objeto = objeto.lower().strip()

    equivalencias = {
        "pocion": "pocion_vida",
        "poción": "pocion_vida",
        "vida": "pocion_vida",

        "energia": "pocion_energia",
        "energía": "pocion_energia",

        "comida": "comida",
    }

    objeto = equivalencias.get(objeto, objeto)

    if objeto not in TIENDA:
        await ctx.send(
            "❌ Ese objeto no está en la tienda."
        )
        return

    producto = TIENDA[objeto]

    await ctx.send(
        f"{producto['nombre']}\n"
        f"💰 Precio: **{formatear_dinero(producto['precio'])} monedas**\n"
        f"📖 {producto['descripcion']}"
    )


# ============================================================
# COMANDO: STOCK / CATÁLOGO
# ============================================================

@commands.command(
    name="catalogo",
    aliases=["catalog", "productos"]
)
async def catalogo(ctx):

    texto = []

    for objeto_id, producto in TIENDA.items():

        texto.append(
            f"{producto['nombre']}\n"
            f"💰 **{formatear_dinero(producto['precio'])}** monedas\n"
            f"📦 `{objeto_id}`"
        )

    embed = discord.Embed(
        title="📦 Catálogo de Foxy",
        description="\n\n".join(texto),
        color=discord.Color.blue()
    )

    await ctx.send(embed=embed)


# ============================================================
# COMANDO ADMIN: AÑADIR PRODUCTO
# ============================================================

@commands.command(name="producto")
@commands.has_permissions(administrator=True)
async def producto(ctx, objeto=None, precio: int = None):

    if objeto is None or precio is None:
        await ctx.send(
            "❌ Uso correcto:\n"
            "`!producto objeto precio`"
        )
        return

    objeto = objeto.lower().strip()

    if objeto not in OBJETOS:
        await ctx.send(
            "❌ Ese objeto no existe en el sistema de inventario."
        )
        return

    if precio <= 0:
        await ctx.send(
            "❌ El precio debe ser mayor que 0."
        )
        return

    nombre = OBJETOS[objeto]["nombre"]
    descripcion = OBJETOS[objeto]["descripcion"]

    TIENDA[objeto] = {
        "precio": precio,
        "nombre": nombre,
        "descripcion": descripcion,
    }

    await ctx.send(
        "🛒 **Producto añadido a la tienda.**\n"
        f"{nombre}\n"
        f"💰 Precio: **{formatear_dinero(precio)} monedas**"
    )


# ============================================================
# ERROR DE PERMISOS
# ============================================================

@producto.error
async def producto_error(ctx, error):

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(
            "❌ Solo los **administradores** pueden "
            "añadir productos."
        )


# ============================================================
# SETUP
# ============================================================

def setup_shop(bot):
    """
    Registra el sistema de tienda.
    """

    bot.add_command(tienda)
    bot.add_command(comprar)
    bot.add_command(precio)
    bot.add_command(catalogo)
    bot.add_command(producto)

    print("🛒 Sistema de Tienda cargado")