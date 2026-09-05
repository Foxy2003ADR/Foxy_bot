# modules/inventory.py

"""
🎒 Foxy Inventory
Sistema de inventario de Foxy.

Este módulo guarda los objetos de Foxy en:
data/inventory.json

La tienda podrá utilizar este sistema para añadir objetos.
El RPG podrá utilizarlo para consumir objetos.
"""

import json
import os

import discord
from discord.ext import commands

from modules.foxy_core import (
    curar,
    recuperar_energia,
)


# ============================================================
# CONFIGURACIÓN
# ============================================================

DATA_DIR = "data"
INVENTORY_FILE = os.path.join(DATA_DIR, "inventory.json")


# ============================================================
# OBJETOS INICIALES
# ============================================================

INVENTARIO_DEFAULT = {
    "pocion_vida": 0,
    "pocion_energia": 0,
    "comida": 0,
}


OBJETOS = {
    "pocion_vida": {
        "nombre": "🧪 Poción de Vida",
        "descripcion": "Restaura 25 puntos de vida.",
        "uso": "vida",
        "cantidad": 25,
    },

    "pocion_energia": {
        "nombre": "⚡ Poción de Energía",
        "descripcion": "Restaura 30 puntos de energía.",
        "uso": "energia",
        "cantidad": 30,
    },

    "comida": {
        "nombre": "🍖 Comida",
        "descripcion": "Restaura 15 puntos de vida y 10 de energía.",
        "uso": "comida",
        "vida": 15,
        "energia": 10,
    },
}


# ============================================================
# ARCHIVOS
# ============================================================

def asegurar_directorio():
    """
    Crea la carpeta data si no existe.
    """
    os.makedirs(DATA_DIR, exist_ok=True)


def guardar_inventario():
    """
    Guarda el inventario en inventory.json.
    """
    asegurar_directorio()

    try:
        with open(INVENTORY_FILE, "w", encoding="utf-8") as archivo:
            json.dump(
                INVENTARIO,
                archivo,
                indent=4,
                ensure_ascii=False
            )

        return True

    except Exception as error:
        print(f"❌ Error guardando inventario: {error}")
        return False


def cargar_inventario():
    """
    Carga el inventario desde inventory.json.
    """

    asegurar_directorio()

    if not os.path.exists(INVENTORY_FILE):
        datos = INVENTARIO_DEFAULT.copy()

        with open(INVENTORY_FILE, "w", encoding="utf-8") as archivo:
            json.dump(
                datos,
                archivo,
                indent=4,
                ensure_ascii=False
            )

        return datos

    try:
        with open(INVENTORY_FILE, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)

        # Añadir objetos nuevos automáticamente.
        for objeto, cantidad in INVENTARIO_DEFAULT.items():
            if objeto not in datos:
                datos[objeto] = cantidad

        return datos

    except Exception as error:
        print(f"⚠️ Error cargando inventario: {error}")

        datos = INVENTARIO_DEFAULT.copy()
        guardar_datos(datos)

        return datos


def guardar_datos(datos):
    """
    Guarda directamente unos datos de inventario.
    """
    asegurar_directorio()

    try:
        with open(INVENTORY_FILE, "w", encoding="utf-8") as archivo:
            json.dump(
                datos,
                archivo,
                indent=4,
                ensure_ascii=False
            )

        return True

    except Exception as error:
        print(f"❌ Error guardando inventario: {error}")
        return False


# ============================================================
# INVENTARIO GLOBAL
# ============================================================

INVENTARIO = cargar_inventario()


# ============================================================
# FUNCIONES DEL INVENTARIO
# ============================================================

def obtener_inventario():
    """
    Devuelve el inventario completo.
    """
    return INVENTARIO


def obtener_cantidad(objeto):
    """
    Devuelve cuántas unidades hay de un objeto.
    """
    return INVENTARIO.get(objeto, 0)


def añadir_objeto(objeto, cantidad=1):
    """
    Añade objetos al inventario.
    """

    if objeto not in OBJETOS:
        return False

    if cantidad <= 0:
        return False

    INVENTARIO[objeto] = INVENTARIO.get(objeto, 0) + cantidad

    guardar_inventario()

    return True


def quitar_objeto(objeto, cantidad=1):
    """
    Quita objetos del inventario si hay suficientes.
    """

    if objeto not in OBJETOS:
        return False

    if cantidad <= 0:
        return False

    if INVENTARIO.get(objeto, 0) < cantidad:
        return False

    INVENTARIO[objeto] -= cantidad

    guardar_inventario()

    return True


def tiene_objeto(objeto, cantidad=1):
    """
    Comprueba si Foxy tiene una cantidad determinada.
    """

    if objeto not in OBJETOS:
        return False

    return INVENTARIO.get(objeto, 0) >= cantidad


# ============================================================
# USAR OBJETOS
# ============================================================

def usar_objeto(objeto):
    """
    Utiliza un objeto del inventario.

    Devuelve:
        (True, mensaje)
    o
        (False, mensaje)
    """

    if objeto not in OBJETOS:
        return False, "❌ Ese objeto no existe."

    if not tiene_objeto(objeto):
        return False, "❌ Foxy no tiene ese objeto."

    datos = OBJETOS[objeto]

    # --------------------------------------------------------
    # POCIÓN DE VIDA
    # --------------------------------------------------------

    if datos["uso"] == "vida":

        cantidad = datos["cantidad"]

        resultado = curar(cantidad)

        if resultado == 0:
            return False, "❤️ Foxy ya tiene la vida al máximo."

        quitar_objeto(objeto)

        return True, (
            f"🧪 Foxy ha usado **{datos['nombre']}**.\n"
            f"❤️ Ha recuperado **+{resultado} de vida**."
        )

    # --------------------------------------------------------
    # POCIÓN DE ENERGÍA
    # --------------------------------------------------------

    if datos["uso"] == "energia":

        cantidad = datos["cantidad"]

        recuperar_energia(cantidad)

        quitar_objeto(objeto)

        return True, (
            f"⚡ Foxy ha usado **{datos['nombre']}**.\n"
            f"⚡ Ha recuperado **+{cantidad} de energía**."
        )

    # --------------------------------------------------------
    # COMIDA
    # --------------------------------------------------------

    if datos["uso"] == "comida":

        vida = datos["vida"]
        energia = datos["energia"]

        vida_recuperada = curar(vida)
        recuperar_energia(energia)

        if vida_recuperada == 0:
            # Aunque la vida esté al máximo,
            # la comida sigue recuperando energía.
            pass

        quitar_objeto(objeto)

        return True, (
            f"🍖 Foxy ha comido **{datos['nombre']}**.\n"
            f"❤️ Vida recuperada: **+{vida_recuperada}**\n"
            f"⚡ Energía recuperada: **+{energia}**"
        )

    return False, "❌ Este objeto todavía no tiene un efecto definido."


# ============================================================
# COMANDO: INVENTARIO
# ============================================================

@commands.command(
    name="inventario",
    aliases=["inv", "mochila"]
)
async def inventario(ctx):

    embed = discord.Embed(
        title="🎒 Inventario de Foxy",
        description="Estos son los objetos que tiene Foxy:",
        color=discord.Color.orange()
    )

    objetos_mostrados = 0

    for objeto_id, datos in OBJETOS.items():

        cantidad = INVENTARIO.get(objeto_id, 0)

        if cantidad > 0:

            embed.add_field(
                name=f"{datos['nombre']} ×{cantidad}",
                value=datos["descripcion"],
                inline=False
            )

            objetos_mostrados += 1

    if objetos_mostrados == 0:
        embed.description = (
            "🎒 El inventario de Foxy está vacío.\n\n"
            "🛒 Puedes conseguir objetos en la tienda."
        )

    await ctx.send(embed=embed)


# ============================================================
# COMANDO: USAR
# ============================================================

@commands.command(
    name="usar",
    aliases=["use"]
)
async def usar(ctx, *, objeto=None):

    if objeto is None:
        await ctx.send(
            "❌ Debes indicar qué objeto quieres usar.\n\n"
            "Ejemplo:\n"
            "`!usar pocion_vida`"
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
        "poción_energía": "pocion_energia",

        "comida": "comida",
        "comer": "comida",
    }

    objeto = equivalencias.get(objeto, objeto)

    correcto, mensaje = usar_objeto(objeto)

    await ctx.send(mensaje)


# ============================================================
# COMANDO: DAR OBJETO
# ============================================================

@commands.command(name="dar_objeto")
@commands.has_permissions(administrator=True)
async def dar_objeto(ctx, objeto=None, cantidad: int = 1):

    if objeto is None:
        await ctx.send(
            "❌ Uso correcto:\n"
            "`!dar_objeto objeto cantidad`"
        )
        return

    objeto = objeto.lower().strip()

    if objeto not in OBJETOS:
        objetos_validos = ", ".join(OBJETOS.keys())

        await ctx.send(
            "❌ Ese objeto no existe.\n\n"
            f"📦 Objetos disponibles:\n`{objetos_validos}`"
        )
        return

    if cantidad <= 0:
        await ctx.send(
            "❌ La cantidad debe ser mayor que **0**."
        )
        return

    añadir_objeto(objeto, cantidad)

    nombre = OBJETOS[objeto]["nombre"]

    await ctx.send(
        f"🎁 **Objeto añadido al inventario de Foxy.**\n"
        f"{nombre} ×**{cantidad}**"
    )


# ============================================================
# COMANDO: QUITAR OBJETO
# ============================================================

@commands.command(name="quitar_objeto")
@commands.has_permissions(administrator=True)
async def quitar_objeto_comando(
    ctx,
    objeto=None,
    cantidad: int = 1
):

    if objeto is None:
        await ctx.send(
            "❌ Uso correcto:\n"
            "`!quitar_objeto objeto cantidad`"
        )
        return

    objeto = objeto.lower().strip()

    if objeto not in OBJETOS:
        await ctx.send(
            "❌ Ese objeto no existe."
        )
        return

    if cantidad <= 0:
        await ctx.send(
            "❌ La cantidad debe ser mayor que **0**."
        )
        return

    if not quitar_objeto(objeto, cantidad):
        await ctx.send(
            "❌ Foxy no tiene suficientes unidades de ese objeto."
        )
        return

    nombre = OBJETOS[objeto]["nombre"]

    await ctx.send(
        f"🗑️ **Objeto retirado del inventario.**\n"
        f"{nombre} ×**{cantidad}**"
    )


# ============================================================
# ERRORES DE PERMISOS
# ============================================================

@dar_objeto.error
async def dar_objeto_error(ctx, error):

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(
            "❌ Solo los **administradores** pueden "
            "dar objetos."
        )


@quitar_objeto_comando.error
async def quitar_objeto_error(ctx, error):

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(
            "❌ Solo los **administradores** pueden "
            "quitar objetos."
        )


# ============================================================
# SETUP
# ============================================================

def setup_inventory(bot):
    """
    Registra el sistema de inventario en el bot.
    """

    asegurar_directorio()
    guardar_inventario()

    bot.add_command(inventario)
    bot.add_command(usar)
    bot.add_command(dar_objeto)
    bot.add_command(quitar_objeto_comando)

    print("🎒 Sistema de Inventario cargado")