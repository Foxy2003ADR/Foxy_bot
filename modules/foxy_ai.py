import discord
from discord.ext import commands
import random
import time


# ============================================================
# 🦊 FOXY AI
# Personalidad de Foxy
# ============================================================

FOXY_NOMBRE = "Foxy"

TWITCH_URL = "https://www.twitch.tv/foxy2003_"
INSTAGRAM_URL = "https://www.instagram.com/_foxy2003_/"

# Tiempo mínimo entre promociones.
# 45 minutos para que no resulte pesado.
PROMO_COOLDOWN = 45 * 60

ultima_promocion = {}


# ============================================================
# 😂 PERSONALIDAD GENERAL
# ============================================================

FOXY_FRASES = [
    "🦊 ¡VAMOS A JUGAR!",
    "🦊 Esto va a salir bien... probablemente. 😈",
    "🦊 Preparad las palomitas, que empieza el espectáculo. 🍿",
    "🦊 Yo no pierdo. Solo hago estrategias alternativas. 😎",
    "🦊 ¿Quién se atreve? 👀",
    "🦊 Hoy venimos a ganar. O al menos a pasarlo bien. 😂",
    "🦊 Vale, concentración máxima. 🧠",
    "🦊 Modo tryhard: ACTIVADO. 🎯",
    "🦊 Tranquilos, tengo un plan. 😎",
    "🦊 El plan está perfecto. Lo que falla es la ejecución. 😂",
    "🦊 Hoy puede pasar cualquier cosa. Y seguramente pase. 💀",
    "🦊 Vamos a ver qué desastre montamos hoy. 😂",
    "🦊 Preparados, que Foxy entra en partida. 🦊🎮",
    "🦊 No prometo ganar, pero prometo espectáculo. 🔥",
    "🦊 Bueno... ¿quién empieza? 👀",
    "🦊 Se viene partidita. 🎮",
    "🦊 Vamos a darlo todo. 💪",
    "🦊 Esto tiene pinta de acabar bien. Creo. 😂",
    "🦊 Hora de demostrar habilidades. 😎",
    "🦊 O de demostrar que no tenemos ninguna. 💀",
]


# ============================================================
# 😎 VACILES SANOS
# ============================================================

FOXY_VACILES = [
    "🦊 Eso ha sido... interesante. 😂",
    "🦊 No pasa nada, todos tenemos nuestros momentos. 😎",
    "🦊 Buena jugada. Te la voy a copiar. 👀",
    "🦊 Vale, esa no me la esperaba. 😂",
    "🦊 ¿Eso estaba planeado? Porque ha quedado increíble. 🔥",
    "🦊 Yo habría hecho exactamente lo mismo... seguramente. 😂",
    "🦊 Aquí hay nivel, señores. 👀",
    "🦊 Bueno bueno bueno... esto se pone interesante. 🔥",
    "🦊 Esa jugada merece repetición. 🎬",
    "🦊 No voy a decir nada... pero lo he visto. 👀",
    "🦊 Tenemos talento en el servidor. 😎",
    "🦊 Eso ha sido bastante limpio. 👌",
    "🦊 Me gusta este equipo. 😂",
    "🦊 Vale, oficialmente esto se está poniendo serio. 🎯",
    "🦊 Yo venía tranquilo y ya estamos compitiendo. 😂",
]


# ============================================================
# 🔥 HYPE
# ============================================================

FOXY_HYPE = [
    "🦊🔥 ¡VAMOOOOOS!",
    "🦊🔥 ¡ESO ES!",
    "🦊🔥 ¡QUÉ JUGADA!",
    "🦊🔥 ¡AHORA SÍ!",
    "🦊🔥 ¡ESTO SE PONE BUENO!",
    "🦊🔥 ¡MENUDO CLUTCH!",
    "🦊🔥 ¡NO PUEDE SER!",
    "🦊🔥 ¡QUÉ LOCURA!",
    "🦊🔥 ¡VAMOS EQUIPO!",
    "🦊🔥 ¡ESTAMOS EN RACHA!",
    "🦊🔥 ¡MODO TRYHARD ACTIVADO!",
    "🦊🔥 ¡ESA ES LA ACTITUD!",
]


# ============================================================
# 😡 RAGE
# ============================================================

FOXY_RAGE = [
    "🦊 ¡¿PERO QUÉ HA PASADO?! 😭",
    "🦊 Esto estaba totalmente calculado... 💀",
    "🦊 NOOOO, ¡ESO NO VALE! 😤",
    "🦊 Necesito hablar con el creador del juego. 😂",
    "🦊 Me retiro dignamente... hasta dentro de 5 minutos. 🫡",
    "🦊 Vale. Respiramos. Seguimos. 😂",
    "🦊 Eso ha dolido más de lo necesario. 💀",
    "🦊 El juego ha decidido que hoy no ganamos. 😭",
    "🦊 Yo estaba jugando perfectamente hasta ese momento. 😂",
    "🦊 Bueno... esa jugada mejor la olvidamos. 🫡",
    "🦊 ¿Quién ha tocado el botón de perder? 😭",
    "🦊 Todo bajo control. Absolutamente todo. 💀",
    "🦊 Estoy perfectamente tranquilo. 😌",
    "🦊 ...Estoy perfectamente tranquilo. 😐",
    "🦊 Vale, eso sí me ha dolido. 😂",
]


# ============================================================
# 💀 MUERTE / FAIL
# ============================================================

FOXY_MUERTE = [
    "🦊💀 Bueno... ha sido una muerte táctica.",
    "🦊💀 Eso no cuenta.",
    "🦊💀 Yo quería comprobar qué había abajo. 😂",
    "🦊💀 La gravedad ha ganado.",
    "🦊💀 Ha sido culpa del teclado. 😭",
    "🦊💀 Estaba mirando otra cosa. 😂",
    "🦊💀 Pequeño fallo técnico.",
    "🦊💀 Esto no ha ocurrido. Seguimos.",
    "🦊💀 Una retirada demasiado rápida.",
    "🦊💀 Bueno... volvemos a intentarlo.",
    "🦊💀 El personaje no tenía muchas ganas de vivir.",
    "🦊💀 Todo calculado. Sí, sí.",
]


# ============================================================
# 🏆 VICTORIA
# ============================================================

FOXY_VICTORIA = [
    "🦊🏆 ¡VICTORIA!",
    "🦊🏆 ¡LO HICIMOS!",
    "🦊🏆 ¡GG! Muy buena partida.",
    "🦊🏆 Eso ha estado bastante bien. 😎",
    "🦊🏆 ¡Victoria para el equipo!",
    "🦊🏆 El plan ha funcionado. 😂",
    "🦊🏆 Hoy sí que hemos venido preparados.",
    "🦊🏆 ¡Partidaza!",
    "🦊🏆 Esto merece otra partida. 👀",
    "🦊🏆 ¡GG equipo!",
]


# ============================================================
# 😭 DERROTA
# ============================================================

FOXY_DERROTA = [
    "🦊😭 Bueno... la próxima es nuestra.",
    "🦊😭 No pasa nada. Se aprende.",
    "🦊😭 Hoy el juego ha ganado.",
    "🦊😭 Ha estado cerca.",
    "🦊😭 GG igualmente. Buena partida.",
    "🦊😭 Nos faltó un poquito de suerte.",
    "🦊😭 Vale, revancha. 😎",
    "🦊😭 Esto pide una segunda partida.",
    "🦊😭 No hemos perdido. Hemos aprendido. 🧠",
    "🦊😭 La siguiente sale mejor.",
]


# ============================================================
# 🏆 GG
# ============================================================

FOXY_GG = [
    "🦊 GG, chavales. ¡Buena partida! 🎮",
    "🦊 ¡GG! Eso ha estado bastante épico. 🔥",
    "🦊 GG EZ... bueno, quizá no tan EZ. 😂",
    "🦊 ¡Buena partida! ¿Otra? 👀",
    "🦊 GG equipo. 🔥",
    "🦊 Muy buena partida. 👌",
    "🦊 GG. Aquí hay nivel. 😎",
    "🦊 ¡GG! Me lo he pasado genial. 🎮",
]


# ============================================================
# 🎯 TRYHARD
# ============================================================

FOXY_TRYHARD = [
    "🦊🎯 Vale, se acabó la broma. Ahora vamos a ganar.",
    "🦊🎯 Concentración.",
    "🦊🎯 Ahora sí: modo competitivo.",
    "🦊🎯 Nada de distraerse.",
    "🦊🎯 Vamos a hacerlo perfecto.",
    "🦊🎯 Cada movimiento cuenta.",
    "🦊🎯 No hemos venido hasta aquí para perder.",
    "🦊🎯 Enfoque total.",
    "🦊🎯 Ahora quiero ver de qué somos capaces.",
    "🦊🎯 Modo tryhard: ON.",
]


# ============================================================
# 😂 FAILS
# ============================================================

FOXY_FAIL = [
    "🦊😂 Eso ha sido un pequeño detalle sin importancia.",
    "🦊😂 Nadie ha visto eso.",
    "🦊😂 Podemos fingir que no ha pasado.",
    "🦊😂 Bueno... técnicamente ha funcionado.",
    "🦊😂 El resultado no era el esperado.",
    "🦊😂 Casi. MUY casi.",
    "🦊😂 Eso en mi cabeza quedaba espectacular.",
    "🦊😂 Mi personaje ha decidido improvisar.",
    "🦊😂 Ha sido contenido de calidad. 😂",
    "🦊😂 Por lo menos nos hemos reído.",
]


# ============================================================
# ❤️ BUEN ROLLO
# ============================================================

FOXY_AMISTAD = [
    "🦊❤️ Buenísima gente.",
    "🦊❤️ Así da gusto jugar.",
    "🦊❤️ Buen equipo.",
    "🦊❤️ Me lo estoy pasando genial.",
    "🦊❤️ Gracias por la partida.",
    "🦊❤️ Este grupo promete.",
    "🦊❤️ Qué buen ambiente.",
    "🦊❤️ Así sí.",
]


# ============================================================
# 👀 CURIOSIDAD
# ============================================================

FOXY_CURIOSO = [
    "🦊👀 ¿Qué estará pasando aquí?",
    "🦊👀 Esto quiero verlo.",
    "🦊👀 Interesante...",
    "🦊👀 Aquí hay algo raro.",
    "🦊👀 Tengo curiosidad.",
    "🦊👀 Esto puede acabar de cualquier manera.",
    "🦊👀 No pienso perderme esto.",
]


# ============================================================
# 🎮 JUEGOS
# ============================================================

FOXY_JUEGOS = {
    "minecraft": [
        "⛏️🦊 Hora de picar bloques hasta que encontremos diamantes.",
        "⛏️🦊 Minecraft: donde cinco minutos pueden convertirse en tres horas.",
        "⛏️🦊 Si desaparecen mis diamantes, tenemos un problema. 😂",
        "⛏️🦊 Construimos primero. Morimos después.",
    ],

    "stardew": [
        "🌾🦊 Hoy toca relajarse... o intentar hacerlo.",
        "🌾🦊 Vamos a convertir esa granja en un imperio.",
        "🌾🦊 Agricultura tryhard. 😂",
        "🌾🦊 ¿Quién necesita dormir cuando hay cosechas?",
    ],

    "terraria": [
        "🧱🦊 Terraria: empezamos tranquilos y acabamos invocando algo horrible.",
        "🧱🦊 Hora de explorar.",
        "🧱🦊 Hoy necesitamos buen loot.",
    ],

    "repo": [
        "👻🦊 R.E.P.O.: entramos, cogemos cosas y esperamos no morir.",
        "👻🦊 Plan sencillo: sobrevivir.",
        "👻🦊 No pasa nada, Foxy controla el miedo. 😂",
        "👻🦊 Si escucháis algo raro, probablemente no sea yo.",
    ],

    "peak": [
        "🏔️🦊 PEAK: subir arriba y no morir. Fácil, ¿no?",
        "🏔️🦊 Vamos a escalar.",
        "🏔️🦊 Si caigo, nadie ha visto nada. 😂",
    ],

    "lethalcompany": [
        "👷🦊 Hora de hacer dinero... y probablemente perder compañeros.",
        "👷🦊 Lethal Company: trabajar duro, morir rápido.",
        "👷🦊 ¿Quién entra primero? 👀",
    ],

    "phasmophobia": [
        "👻🦊 Phasmophobia: hoy toca hablar con fantasmas.",
        "👻🦊 Yo no tengo miedo. Bueno... un poquito.",
        "👻🦊 Si corro, corréis conmigo. 😂",
    ],

    "contentwarning": [
        "📹🦊 Vamos a grabar contenido de calidad.",
        "📹🦊 Lo importante no es sobrevivir. Es conseguir visitas. 😂",
        "📹🦊 Esto tiene pinta de buen clip.",
    ],

    "valheim": [
        "🛡️🦊 Valheim: supervivencia, exploración y probablemente algún susto.",
        "🛡️🦊 Vamos a construir algo épico.",
    ],

    "ark": [
        "🦖🦊 ARK: vamos a domesticar dinosaurios.",
        "🦖🦊 Nada puede salir mal con dinosaurios. 😂",
        "🦖🦊 Necesitamos una base enorme.",
    ],

    "palworld": [
        "🦕🦊 Palworld: hora de conseguir unos cuantos Pals.",
        "🦕🦊 Vamos a montar nuestro imperio.",
    ],

    "rust": [
        "🔧🦊 Rust: confianza cero, supervivencia cien.",
        "🔧🦊 No confiéis en nadie. 😂",
        "🔧🦊 Construimos rápido y pensamos después.",
    ],

    "projectzomboid": [
        "🧟🦊 Project Zomboid: objetivo número uno, no morir.",
        "🧟🦊 Un pequeño error aquí puede acabar fatal.",
    ],

    "dontstarvetogether": [
        "🍖🦊 Don't Starve Together: literalmente no hay que morir de hambre.",
        "🍖🦊 Primero comida. Después aventuras.",
    ],

    "7daystodie": [
        "🧟🦊 Tenemos siete días para prepararnos.",
        "🧟🦊 La noche promete.",
    ],

    "nomanssky": [
        "🌌🦊 Nos vamos al espacio.",
        "🌌🦊 Hora de explorar planetas.",
    ],

    "seaofthieves": [
        "🏴‍☠️🦊 ¡TODOS A BORDO!",
        "🏴‍☠️🦊 Hoy somos piratas.",
        "🏴‍☠️🦊 Cuidado con los barcos enemigos. 👀",
    ],

    "cs2": [
        "💥🦊 CS2: concentración máxima.",
        "💥🦊 Una bala, una oportunidad.",
        "💥🦊 Vamos a buscar ese clutch.",
    ],

    "valorant": [
        "🎯🦊 Valorant: ahora sí toca tryhard.",
        "🎯🦊 Precisión máxima.",
        "🎯🦊 Vamos por esa victoria.",
    ],

    "fortnite": [
        "🪂🦊 Fortnite: ¿quién quiere una victoria?",
        "🪂🦊 Aterrizamos y empezamos.",
        "🪂🦊 Hoy toca intentar llevarnos la partida.",
    ],

    "apex": [
        "🔫🦊 Apex: velocidad y puntería.",
        "🔫🦊 Vamos a buscar esa partida perfecta.",
    ],

    "overwatch": [
        "🦸🦊 Overwatch: necesitamos coordinación.",
        "🦸🦊 Equipo unido, partida ganada.",
    ],

    "rainbowsix": [
        "🏰🦊 Rainbow Six: aquí hay que pensar.",
        "🏰🦊 Ojos abiertos y concentración.",
    ],

    "callofduty": [
        "💣🦊 Call of Duty: vamos a darle.",
        "💣🦊 Hora de entrar en acción.",
    ],

    "pubg": [
        "🪖🦊 PUBG: supervivencia hasta el final.",
        "🪖🦊 Hay que jugar inteligente.",
    ],

    "marvelrivals": [
        "🦸🦊 Marvel Rivals: vamos a salvar el mundo.",
        "🦸🦊 Hoy toca demostrar quién manda.",
    ],

    "tf2": [
        "🔫🦊 Team Fortress 2: caos asegurado.",
        "🔫🦊 Esto puede ponerse muy loco.",
    ],

    "deltaforce": [
        "⚡🦊 Delta Force: vamos al combate.",
        "⚡🦊 Concentración y a por ellos.",
    ],

    "amongus": [
        "ඞ🦊 Among Us: aquí no se puede confiar en nadie.",
        "🔪🔴🦊 ¿Quién será el impostor?",
        "ඞ🦊 Yo soy inocente. Totalmente. 👀",
        "ඞ🦊 Si me votáis, os vais a arrepentir. 😂",
    ],

    "roblox": [
        "🧱🦊 Roblox: nunca sabes qué vas a jugar.",
        "🧱🦊 Hoy toca descubrir alguna locura.",
    ],

    "fallguys": [
        "🥚🦊 Fall Guys: equilibrio y sufrimiento.",
        "🥚🦊 Hoy no nos caemos. Espero.",
    ],

    "gmod": [
        "🔧🦊 Garry's Mod: el caos empieza ahora.",
        "🔧🦊 Aquí las leyes de la física son opcionales.",
    ],

    "humanfallflat": [
        "🧍🦊 Human Fall Flat: coordinación máxima. 😂",
        "🧍🦊 Caminar ya va a ser un reto.",
    ],

    "gangbeasts": [
        "🕺🦊 Gang Beasts: hoy toca repartir abrazos... violentos. 😂",
        "🕺🦊 Que empiece el caos.",
    ],

    "partyanimals": [
        "🐶🦊 Party Animals: preparados para el caos.",
        "🐶🦊 Hoy nadie sale limpio. 😂",
    ],

    "pummelparty": [
        "🎉🦊 Pummel Party: amistades en peligro. 😂",
        "🎉🦊 Todo por ganar.",
    ],

    "golfwithyourfriends": [
        "⛳🦊 Golf con amigos: fácil hasta que intentas meterla.",
        "⛳🦊 Hoy buscamos el hoyo perfecto.",
    ],

    "jackbox": [
        "🎤🦊 Jackbox: aquí gana la creatividad.",
        "🎤🦊 A ver quién tiene las mejores respuestas.",
    ],

    "rocketleague": [
        "🚗🦊 Rocket League: coches + fútbol = caos.",
        "🚗🦊 Hoy toca marcar golazos.",
        "🚗🦊 Si hago un gol aéreo, me retiro. 😂",
    ],

    "forza": [
        "🏎️🦊 Forza Horizon: pisamos el acelerador.",
        "🏎️🦊 Vamos a buscar el coche más rápido.",
    ],

    "fc": [
        "⚽🦊 EA Sports FC: hora de demostrar quién sabe jugar.",
        "⚽🦊 Vamos a por ese gol.",
    ],

    "gtav": [
        "🚗🦊 GTA V: hoy puede pasar absolutamente cualquier cosa.",
        "🚗🦊 Vamos a liarla... con moderación. 😂",
    ],

    "eldenring": [
        "⚔️🦊 Elden Ring: paciencia y sufrimiento.",
        "⚔️🦊 Hoy derrotamos a ese jefe.",
    ],

    "baldursgate3": [
        "🐉🦊 Baldur's Gate 3: decisiones cuestionables incoming.",
        "🐉🦊 Vamos a ver qué aventura nos espera.",
    ],

    "genshin": [
        "✨🦊 Genshin Impact: toca explorar.",
        "✨🦊 Hora de conseguir buen loot.",
    ],

    "warframe": [
        "⚔️🦊 Warframe: velocidad máxima.",
        "⚔️🦊 Vamos a repartir estopa.",
    ],

    "helldivers2": [
        "💥🦊 Helldivers 2: ¡POR LA DEMOCRACIA!",
        "💥🦊 Soldados, preparados.",
    ],

    "deadbydaylight": [
        "☠️🦊 Dead by Daylight: hoy toca sobrevivir.",
        "☠️🦊 Espero que el killer tenga piedad. 😂",
        "☠️🦊 Si escucháis el corazón, corred.",
    ],
}


# ============================================================
# 🎯 RETOS
# ============================================================

FOXY_RETOS = [
    "🎯 Consigue una victoria sin morir.",
    "😂 Haz la jugada más absurda que puedas.",
    "💀 Si mueres, toca revancha.",
    "🔥 Intenta superar tu récord.",
    "😈 Juega como si fueras el protagonista.",
    "🧠 Gana usando una estrategia completamente distinta.",
    "🎯 Intenta conseguir una jugada perfecta.",
    "🔥 Consigue una victoria jugando en modo tryhard.",
    "😂 Haz algo que normalmente nunca harías.",
    "👀 Intenta sorprender al resto del grupo.",
    "💪 No abandones hasta terminar la partida.",
    "🏆 Intenta quedar primero.",
    "🎮 Juega durante una partida sin cometer errores.",
    "😎 Confía en tu estrategia.",
    "🧠 Piensa antes de actuar.",
]


# ============================================================
# 📢 PROMOCIÓN
# ============================================================

FOXY_PROMOCIONES = [
    (
        "🎥 **¿Queréis divertiros conmigo en directo?**\n"
        f"🦊 Twitch: {TWITCH_URL}"
    ),
    (
        "🎥 **Si queréis pasaros por algún directo, os espero por Twitch.**\n"
        f"🦊 {TWITCH_URL}"
    ),
    (
        "📸 **Y si queréis ver más momentos de Foxy fuera de directo:**\n"
        f"🦊 Instagram: {INSTAGRAM_URL}"
    ),
    (
        "🦊 **Para más partidas, momentos y locuras:**\n"
        f"🎥 Twitch: {TWITCH_URL}\n"
        f"📸 Instagram: {INSTAGRAM_URL}"
    ),
]


def puede_promocionar(guild_id):
    ahora = time.time()
    ultima = ultima_promocion.get(guild_id, 0)

    return ahora - ultima >= PROMO_COOLDOWN


def registrar_promocion(guild_id):
    ultima_promocion[guild_id] = time.time()


async def promocion_ocasional(ctx):
    """
    Promoción muy ocasional.
    No aparece siempre.
    """

    if not puede_promocionar(ctx.guild.id):
        return

    # Solo 8% de posibilidades.
    if random.randint(1, 100) > 8:
        return

    mensaje = random.choice(FOXY_PROMOCIONES)

    await ctx.send(mensaje)

    registrar_promocion(ctx.guild.id)


# ============================================================
# 🎮 FUNCIONES
# ============================================================

async def foxy_jugar(ctx):
    frase = random.choice(FOXY_FRASES)

    embed = discord.Embed(
        title="🦊🎮 FOXY ESTÁ JUGANDO",
        description=(
            f"{frase}\n\n"
            "🎮 Foxy está preparado para jugar.\n"
            "👀 ¿Quién se apunta?"
        ),
        color=discord.Color.purple()
    )

    await ctx.send(embed=embed)

    await promocion_ocasional(ctx)


async def foxy_reto(ctx):
    reto = random.choice(FOXY_RETOS)

    embed = discord.Embed(
        title="🦊🔥 RETO DE FOXY",
        description=(
            "**Tu reto es:**\n\n"
            f"{reto}\n\n"
            "🦊 Buena suerte... la vas a necesitar."
        ),
        color=discord.Color.orange()
    )

    await ctx.send(embed=embed)


async def foxy_dado(ctx):
    resultado = random.randint(1, 6)

    caras = {
        1: "⚀",
        2: "⚁",
        3: "⚂",
        4: "⚃",
        5: "⚄",
        6: "⚅",
    }

    await ctx.send(
        f"🦊🎲 Foxy ha tirado el dado...\n\n"
        f"**{caras[resultado]} {resultado}**"
    )


async def foxy_moneda(ctx):
    resultado = random.choice(["🪙 Cara", "🪙 Cruz"])

    await ctx.send(
        f"🦊🪙 Foxy lanza la moneda...\n\n"
        f"**{resultado}**"
    )


async def foxy_suerte(ctx):
    porcentaje = random.randint(1, 100)

    if porcentaje >= 90:
        comentario = "🔥 Hoy estás tocado por los dioses."
    elif porcentaje >= 75:
        comentario = "😎 Hoy vienes fuerte."
    elif porcentaje >= 50:
        comentario = "👍 Puede salir bien."
    elif porcentaje >= 25:
        comentario = "🤔 No está muy claro..."
    else:
        comentario = "💀 Mejor ni juegues."

    await ctx.send(
        f"🦊🍀 **Nivel de suerte de Foxy:**\n\n"
        f"**{porcentaje}%**\n\n"
        f"{comentario}"
    )


async def foxy_rage(ctx):
    await ctx.send(random.choice(FOXY_RAGE))


async def foxy_gg(ctx):
    await ctx.send(random.choice(FOXY_GG))


async def foxy_victoria(ctx):
    await ctx.send(random.choice(FOXY_VICTORIA))


async def foxy_derrota(ctx):
    await ctx.send(random.choice(FOXY_DERROTA))


async def foxy_muerte(ctx):
    await ctx.send(random.choice(FOXY_MUERTE))


async def foxy_fail(ctx):
    await ctx.send(random.choice(FOXY_FAIL))


async def foxy_hype(ctx):
    await ctx.send(random.choice(FOXY_HYPE))


async def foxy_tryhard(ctx):
    await ctx.send(random.choice(FOXY_TRYHARD))


async def foxy_vacile(ctx):
    await ctx.send(random.choice(FOXY_VACILES))


async def foxy_amigo(ctx):
    await ctx.send(random.choice(FOXY_AMISTAD))


async def foxy_curioso(ctx):
    await ctx.send(random.choice(FOXY_CURIOSO))


async def foxy_juego(ctx, juego):
    juego = juego.lower().replace(" ", "")

    # Alias para nombres escritos de diferentes formas.
    alias = {
        "minecraft": "minecraft",
        "stardew": "stardew",
        "stardewvalley": "stardew",
        "terraria": "terraria",
        "repo": "repo",
        "r.e.p.o.": "repo",
        "peak": "peak",
        "lethal": "lethalcompany",
        "lethalcompany": "lethalcompany",
        "phasmophobia": "phasmophobia",
        "contentwarning": "contentwarning",
        "valheim": "valheim",
        "ark": "ark",
        "palworld": "palworld",
        "rust": "rust",
        "projectzomboid": "projectzomboid",
        "7daystodie": "7daystodie",
        "nomanssky": "nomansky",
        "seaofthieves": "seaofthieves",
        "cs2": "cs2",
        "counterstrike2": "cs2",
        "valorant": "valorant",
        "fortnite": "fortnite",
        "apex": "apex",
        "apexlegends": "apex",
        "overwatch": "overwatch",
        "overwatch2": "overwatch",
        "rainbowsix": "rainbowsix",
        "rainbowsixsiege": "rainbowsix",
        "callofduty": "callofduty",
        "cod": "callofduty",
        "pubg": "pubg",
        "marvelrivals": "marvelrivals",
        "tf2": "tf2",
        "teamfortress2": "tf2",
        "deltaforce": "deltaforce",
        "amongus": "amongus",
        "among": "amongus",
        "roblox": "roblox",
        "fallguys": "fallguys",
        "gmod": "gmod",
        "garrysmod": "gmod",
        "humanfallflat": "humanfallflat",
        "gangbeasts": "gangbeasts",
        "partyanimals": "partyanimals",
        "pummelparty": "pummelparty",
        "golfwithyourfriends": "golfwithyourfriends",
        "jackbox": "jackbox",
        "rocketleague": "rocketleague",
        "forza": "forza",
        "forzahorizon": "forza",
        "fc": "fc",
        "easportsfc": "fc",
        "gtav": "gtav",
        "gta": "gtav",
        "eldenring": "eldenring",
        "baldursgate3": "baldursgate3",
        "genshin": "genshin",
        "genshinimpact": "genshin",
        "warframe": "warframe",
        "helldivers": "helldivers2",
        "helldivers2": "helldivers2",
        "deadbydaylight": "deadbydaylight",
        "dbd": "deadbydaylight",
    }

    clave = alias.get(juego)

    if clave is None or clave not in FOXY_JUEGOS:
        await ctx.send(
            "🦊🎮 Ese juego todavía no tiene personalidad propia.\n"
            "Prueba con otro de los juegos disponibles."
        )
        return

    await ctx.send(random.choice(FOXY_JUEGOS[clave]))

    await promocion_ocasional(ctx)


# ============================================================
# 📋 AYUDA
# ============================================================

def ayuda_foxy():
    return (
        "🦊 **FOXY AI**\n\n"
        "🎮 `!foxy jugar` — Foxy se prepara para jugar\n"
        "🔥 `!foxy reto` — Reto aleatorio\n"
        "🎲 `!foxy dado` — Tirar un dado\n"
        "🪙 `!foxy moneda` — Cara o cruz\n"
        "🍀 `!foxy suerte` — Comprueba tu suerte\n"
        "😡 `!foxy rage` — Momento rage\n"
        "🏆 `!foxy gg` — GG de Foxy\n"
        "🏆 `!foxy victoria` — Celebrar victoria\n"
        "😭 `!foxy derrota` — Reaccionar a una derrota\n"
        "💀 `!foxy muerte` — Reaccionar a una muerte\n"
        "😂 `!foxy fail` — Reaccionar a un fail\n"
        "🔥 `!foxy hype` — Subir el hype\n"
        "🎯 `!foxy tryhard` — Modo tryhard\n"
        "😎 `!foxy vacile` — Vacile sano\n"
        "❤️ `!foxy buenrollo` — Buen rollo\n"
        "👀 `!foxy curioso` — Foxy tiene curiosidad\n"
        "🎮 `!foxy juego <juego>` — Frase específica del juego\n\n"
        "📢 Las promociones de redes aparecen ocasionalmente."
    )


# ============================================================
# 🤖 SETUP
# ============================================================

def setup_foxy_ai(bot):

    @bot.command(name="foxy")
    async def foxy(ctx, accion=None, *, argumento=None):

        if accion is None:
            await ctx.send(ayuda_foxy())
            return

        accion = accion.lower().strip()

        if accion == "jugar":
            await foxy_jugar(ctx)

        elif accion == "reto":
            await foxy_reto(ctx)

        elif accion == "dado":
            await foxy_dado(ctx)

        elif accion == "moneda":
            await foxy_moneda(ctx)

        elif accion == "suerte":
            await foxy_suerte(ctx)

        elif accion == "rage":
            await foxy_rage(ctx)

        elif accion == "gg":
            await foxy_gg(ctx)

        elif accion == "victoria":
            await foxy_victoria(ctx)

        elif accion == "derrota":
            await foxy_derrota(ctx)

        elif accion == "muerte":
            await foxy_muerte(ctx)

        elif accion == "fail":
            await foxy_fail(ctx)

        elif accion == "hype":
            await foxy_hype(ctx)

        elif accion == "tryhard":
            await foxy_tryhard(ctx)

        elif accion == "vacile":
            await foxy_vacile(ctx)

        elif accion in ["buenrollo", "amigo", "amistad"]:
            await foxy_amigo(ctx)

        elif accion == "curioso":
            await foxy_curioso(ctx)

        elif accion == "juego":

            if argumento is None:
                await ctx.send(
                    "🦊🎮 Dime qué juego quieres.\n"
                    "Ejemplo: `!foxy juego minecraft`"
                )
                return

            await foxy_juego(ctx, argumento)

        else:
            await ctx.send(
                "🦊 No conozco ese comando.\n\n"
                "Usa `!foxy` para ver todo lo que puedo hacer."
            )


# ============================================================
# 🦊 FIN DE FOXY AI
# ============================================================