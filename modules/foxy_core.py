# modules/foxy_core.py

"""
🦊 Foxy Core
Sistema central de Foxy.

Aquí se guarda y gestiona:
- Nivel
- XP
- Dinero
- Vida
- Energía
- Estado
- Partidas
- Victorias
- Derrotas
- Rachas

Los demás módulos (RPG, Economía, etc.)
utilizan este sistema en lugar de crear datos duplicados.
"""

import json
import os


# ============================================================
# CONFIGURACIÓN
# ============================================================

FOXY_ID = "foxy_virtual"
FOXY_NOMBRE = "Foxy"

DATA_DIR = "data"
FOXY_FILE = os.path.join(DATA_DIR, "foxy.json")


# ============================================================
# DATOS POR DEFECTO
# ============================================================

FOXY_DEFAULT = {
    "id": FOXY_ID,
    "nombre": FOXY_NOMBRE,

    "nivel": 1,
    "xp": 0,

    "dinero": 0,

    "vida": 100,
    "vida_max": 100,

    "energia": 100,
    "energia_max": 100,

    "estado": "Feliz",

    "partidas": 0,
    "victorias": 0,
    "derrotas": 0,

    "racha": 0,
    "mejor_racha": 0
}


# ============================================================
# ARCHIVOS
# ============================================================

def asegurar_directorio():
    """
    Crea la carpeta data si no existe.
    """
    os.makedirs(DATA_DIR, exist_ok=True)


def guardar_foxy():
    """
    Guarda los datos actuales de Foxy en foxy.json.
    """
    asegurar_directorio()

    try:
        with open(FOXY_FILE, "w", encoding="utf-8") as archivo:
            json.dump(
                FOXY,
                archivo,
                indent=4,
                ensure_ascii=False
            )

        return True

    except Exception as error:
        print(f"❌ Error guardando Foxy: {error}")
        return False


def cargar_foxy():
    """
    Carga los datos de Foxy desde foxy.json.

    Si no existe el archivo, crea los datos por defecto.
    """

    asegurar_directorio()

    if not os.path.exists(FOXY_FILE):
        datos = FOXY_DEFAULT.copy()
        guardar_datos(datos)
        return datos

    try:
        with open(FOXY_FILE, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)

        # Añadir automáticamente cualquier dato nuevo
        # que exista en los valores por defecto.
        for clave, valor in FOXY_DEFAULT.items():
            if clave not in datos:
                datos[clave] = valor

        return datos

    except Exception as error:
        print(f"⚠️ Error cargando Foxy: {error}")
        print("🦊 Se utilizarán los datos por defecto.")

        datos = FOXY_DEFAULT.copy()
        guardar_datos(datos)
        return datos


def guardar_datos(datos):
    """
    Guarda directamente un diccionario de datos.
    """
    asegurar_directorio()

    try:
        with open(FOXY_FILE, "w", encoding="utf-8") as archivo:
            json.dump(
                datos,
                archivo,
                indent=4,
                ensure_ascii=False
            )

        return True

    except Exception as error:
        print(f"❌ Error guardando datos: {error}")
        return False


# ============================================================
# DATOS GLOBALES
# ============================================================

FOXY = cargar_foxy()


# ============================================================
# ACCESO A FOXY
# ============================================================

def obtener_foxy():
    """
    Devuelve los datos actuales de Foxy.
    """
    return FOXY


def reiniciar_foxy():
    """
    Reinicia todos los datos de Foxy.
    """
    global FOXY

    FOXY = FOXY_DEFAULT.copy()
    guardar_foxy()

    return FOXY


# ============================================================
# XP Y NIVEL
# ============================================================

def xp_necesaria_para_nivel(nivel):
    """
    Calcula la XP necesaria para alcanzar el siguiente nivel.
    """

    if nivel < 1:
        nivel = 1

    return nivel * 100


def añadir_xp(cantidad):
    """
    Añade XP a Foxy y sube de nivel automáticamente
    cuando alcanza la cantidad necesaria.
    """

    if cantidad <= 0:
        return False

    FOXY["xp"] += cantidad

    subidas = 0

    while FOXY["xp"] >= xp_necesaria_para_nivel(FOXY["nivel"]):
        necesaria = xp_necesaria_para_nivel(FOXY["nivel"])

        FOXY["xp"] -= necesaria
        FOXY["nivel"] += 1
        subidas += 1

    guardar_foxy()

    return subidas


# ============================================================
# DINERO
# ============================================================

def añadir_dinero(cantidad):
    """
    Añade dinero a Foxy.
    """

    if cantidad <= 0:
        return False

    FOXY["dinero"] += cantidad

    guardar_foxy()

    return True


def quitar_dinero(cantidad):
    """
    Quita dinero de Foxy si tiene suficiente.
    """

    if cantidad <= 0:
        return False

    if FOXY["dinero"] < cantidad:
        return False

    FOXY["dinero"] -= cantidad

    guardar_foxy()

    return True


# ============================================================
# VIDA
# ============================================================

def curar(cantidad):
    """
    Cura a Foxy sin superar su vida máxima.
    """

    if cantidad <= 0:
        return False

    vida_anterior = FOXY["vida"]

    FOXY["vida"] = min(
        FOXY["vida"] + cantidad,
        FOXY["vida_max"]
    )

    guardar_foxy()

    return FOXY["vida"] - vida_anterior


def recibir_daño(cantidad):
    """
    Hace daño a Foxy sin bajar de 0 de vida.
    """

    if cantidad <= 0:
        return False

    FOXY["vida"] = max(
        FOXY["vida"] - cantidad,
        0
    )

    guardar_foxy()

    return True


# ============================================================
# ENERGÍA
# ============================================================

def gastar_energia(cantidad):
    """
    Gasta energía si Foxy tiene suficiente.
    """

    if cantidad <= 0:
        return False

    if FOXY["energia"] < cantidad:
        return False

    FOXY["energia"] -= cantidad

    guardar_foxy()

    return True


def recuperar_energia(cantidad):
    """
    Recupera energía sin superar el máximo.
    """

    if cantidad <= 0:
        return False

    FOXY["energia"] = min(
        FOXY["energia"] + cantidad,
        FOXY["energia_max"]
    )

    guardar_foxy()

    return True


# ============================================================
# ESTADO
# ============================================================

def cambiar_estado(estado):
    """
    Cambia el estado de Foxy.
    """

    if not estado:
        return False

    FOXY["estado"] = estado

    guardar_foxy()

    return True


# ============================================================
# PARTIDAS
# ============================================================

def registrar_partida(victoria=False):
    """
    Registra una partida de Foxy.

    Si victoria=True:
        - Suma una victoria.
        - Aumenta la racha.

    Si victoria=False:
        - Suma una derrota.
        - Reinicia la racha.
    """

    FOXY["partidas"] += 1

    if victoria:
        FOXY["victorias"] += 1
        FOXY["racha"] += 1

        if FOXY["racha"] > FOXY["mejor_racha"]:
            FOXY["mejor_racha"] = FOXY["racha"]

    else:
        FOXY["derrotas"] += 1
        FOXY["racha"] = 0

    guardar_foxy()

    return True


# ============================================================
# ESTADÍSTICAS
# ============================================================

def obtener_estadisticas():
    """
    Devuelve las estadísticas principales de Foxy.
    """

    return {
        "nivel": FOXY["nivel"],
        "xp": FOXY["xp"],
        "dinero": FOXY["dinero"],
        "vida": FOXY["vida"],
        "vida_max": FOXY["vida_max"],
        "energia": FOXY["energia"],
        "energia_max": FOXY["energia_max"],
        "estado": FOXY["estado"],
        "partidas": FOXY["partidas"],
        "victorias": FOXY["victorias"],
        "derrotas": FOXY["derrotas"],
        "racha": FOXY["racha"],
        "mejor_racha": FOXY["mejor_racha"]
    }


def obtener_perfil():
    """
    Devuelve una copia completa del perfil de Foxy.
    """
    return FOXY.copy()


# ============================================================
# RESUMEN
# ============================================================

def resumen_foxy():
    """
    Devuelve un resumen de Foxy en formato de texto.
    """

    return (
        f"🦊 Foxy\n"
        f"⭐ Nivel: {FOXY['nivel']}\n"
        f"✨ XP: {FOXY['xp']}/{xp_necesaria_para_nivel(FOXY['nivel'])}\n"
        f"💰 Dinero: {FOXY['dinero']}\n"
        f"❤️ Vida: {FOXY['vida']}/{FOXY['vida_max']}\n"
        f"⚡ Energía: {FOXY['energia']}/{FOXY['energia_max']}\n"
        f"😊 Estado: {FOXY['estado']}\n"
        f"🎮 Partidas: {FOXY['partidas']}\n"
        f"🏆 Victorias: {FOXY['victorias']}\n"
        f"💀 Derrotas: {FOXY['derrotas']}\n"
        f"🔥 Racha: {FOXY['racha']}\n"
        f"👑 Mejor racha: {FOXY['mejor_racha']}"
    )


# ============================================================
# SETUP
# ============================================================

def setup_foxy_core(bot):
    """
    Inicializa el sistema central de Foxy.

    Este módulo no registra comandos.
    Solo prepara y carga los datos.
    """

    asegurar_directorio()
    guardar_foxy()

    print("🦊 Sistema Foxy Core cargado")