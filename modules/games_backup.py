import random

import discord
from discord.ext import commands


# ============================================================
# JUEGOS
# ============================================================

GAMES = {
    # --------------------------------------------------------
    # SUPERVIVENCIA / COOPERATIVO
    # --------------------------------------------------------

    "minecraft": {
        "emoji": "⛏️",
        "name": "Minecraft",
        "category": "Supervivencia",
        "description": "Busca gente para jugar Minecraft."
    },

    "stardew": {
        "emoji": "🌱",
        "name": "Stardew Valley",
        "category": "Supervivencia",
        "description": "Busca gente para jugar Stardew Valley."
    },

    "terraria": {
        "emoji": "🧱",
        "name": "Terraria",
        "category": "Supervivencia",
        "description": "Busca gente para jugar Terraria."
    },

    "repo": {
        "emoji": "👻",
        "name": "R.E.P.O.",
        "category": "Supervivencia",
        "description": "Busca gente para jugar R.E.P.O."
    },

    "peak": {
        "emoji": "🏔️",
        "name": "PEAK",
        "category": "Supervivencia",
        "description": "Busca gente para escalar y sobrevivir en PEAK."
    },

    "lethalcompany": {
        "emoji": "👽",
        "name": "Lethal Company",
        "category": "Supervivencia",
        "description": "Busca gente para jugar Lethal Company."
    },

    "phasmophobia": {
        "emoji": "👻",
        "name": "Phasmophobia",
        "category": "Supervivencia",
        "description": "Busca gente para investigar fantasmas."
    },

    "contentwarning": {
        "emoji": "📹",
        "name": "Content Warning",
        "category": "Supervivencia",
        "description": "Busca gente para grabar cosas terroríficas."
    },

    "valheim": {
        "emoji": "⚔️",
        "name": "Valheim",
        "category": "Supervivencia",
        "description": "Busca vikingos para sobrevivir juntos."
    },

    "ark": {
        "emoji": "🦖",
        "name": "ARK",
        "category": "Supervivencia",
        "description": "Busca gente para sobrevivir entre dinosaurios."
    },

    "palworld": {
        "emoji": "🐾",
        "name": "Palworld",
        "category": "Supervivencia",
        "description": "Busca gente para explorar Palworld."
    },

    "rust": {
        "emoji": "🔨",
        "name": "Rust",
        "category": "Supervivencia",
        "description": "Busca gente para sobrevivir en Rust."
    },

    "projectzomboid": {
        "emoji": "🧟",
        "name": "Project Zomboid",
        "category": "Supervivencia",
        "description": "Busca supervivientes para luchar contra zombis."
    },

    "dontstarvetogether": {
        "emoji": "🔥",
        "name": "Don't Starve Together",
        "category": "Supervivencia",
        "description": "Busca gente para sobrevivir juntos."
    },

    "7daystodie": {
        "emoji": "🧟",
        "name": "7 Days to Die",
        "category": "Supervivencia",
        "description": "Busca gente para sobrevivir al apocalipsis."
    },

    "nomanssky": {
        "emoji": "🚀",
        "name": "No Man's Sky",
        "category": "Supervivencia",
        "description": "Busca exploradores espaciales."
    },

    "seaofthieves": {
        "emoji": "🏴‍☠️",
        "name": "Sea of Thieves",
        "category": "Supervivencia",
        "description": "Busca tripulación para navegar juntos."
    },

    # --------------------------------------------------------
    # COMPETITIVOS
    # --------------------------------------------------------

    "cs2": {
        "emoji": "🔫",
        "name": "Counter-Strike 2",
        "category": "Competitivos",
        "description": "Busca compañeros para jugar CS2."
    },

    "valorant": {
        "emoji": "🎯",
        "name": "Valorant",
        "category": "Competitivos",
        "description": "Busca compañeros para jugar Valorant."
    },

    "fortnite": {
        "emoji": "🔫",
        "name": "Fortnite",
        "category": "Competitivos",
        "description": "Busca escuadra para jugar Fortnite."
    },

    "apex": {
        "emoji": "🏹",
        "name": "Apex Legends",
        "category": "Competitivos",
        "description": "Busca compañeros para Apex Legends."
    },

    "overwatch": {
        "emoji": "🦸",
        "name": "Overwatch 2",
        "category": "Competitivos",
        "description": "Busca equipo para Overwatch 2."
    },

    "rainbowsix": {
        "emoji": "🛡️",
        "name": "Rainbow Six Siege",
        "category": "Competitivos",
        "description": "Busca compañeros para Rainbow Six Siege."
    },

    "callofduty": {
        "emoji": "🪖",
        "name": "Call of Duty",
        "category": "Competitivos",
        "description": "Busca compañeros para Call of Duty."
    },

    "pubg": {
        "emoji": "🪖",
        "name": "PUBG",
        "category": "Competitivos",
        "description": "Busca escuadra para PUBG."
    },

    "marvelrivals": {
        "emoji": "🦸",
        "name": "Marvel Rivals",
        "category": "Competitivos",
        "description": "Busca equipo para Marvel Rivals."
    },

    "tf2": {
        "emoji": "💥",
        "name": "Team Fortress 2",
        "category": "Competitivos",
        "description": "Busca compañeros para Team Fortress 2."
    },

    "deltaforce": {
        "emoji": "🎖️",
        "name": "Delta Force",
        "category": "Competitivos",
        "description": "Busca compañeros para Delta Force."
    },

    # --------------------------------------------------------
    # PARTY / AMIGOS
    # --------------------------------------------------------

    "amongus": {
        "emoji": "🔪",
        "name": "Among Us",
        "category": "Party",
        "description": "🔴 Busca tripulación para Among Us."
    },

    "roblox": {
        "emoji": "🧱",
        "name": "Roblox",
        "category": "Party",
        "description": "Busca gente para jugar Roblox."
    },

    "fallguys": {
        "emoji": "🏃",
        "name": "Fall Guys",
        "category": "Party",
        "description": "Busca gente para jugar Fall Guys."
    },

    "gmod": {
        "emoji": "🔧",
        "name": "Garry's Mod",
        "category": "Party",
        "description": "Busca gente para jugar Garry's Mod."
    },

    "humanfallflat": {
        "emoji": "🧍",
        "name": "Human: Fall Flat",
        "category": "Party",
        "description": "Busca gente para jugar Human: Fall Flat."
    },

    "gangbeasts": {
        "emoji": "🥊",
        "name": "Gang Beasts",
        "category": "Party",
        "description": "Busca gente para liarla en Gang Beasts."
    },

    "partyanimals": {
        "emoji": "🐶",
        "name": "Party Animals",
        "category": "Party",
        "description": "Busca gente para jugar Party Animals."
    },

    "pummelparty": {
        "emoji": "🎲",
        "name": "Pummel Party",
        "category": "Party",
        "description": "Busca gente para jugar Pummel Party."
    },

    "golfwithyourfriends": {
        "emoji": "⛳",
        "name": "Golf With Your Friends",
        "category": "Party",
        "description": "Busca gente para jugar al golf."
    },

    "jackbox": {
        "emoji": "🎤",
        "name": "Jackbox Party Pack",
        "category": "Party",
        "description": "Busca gente para jugar Jackbox."
    },

    # --------------------------------------------------------
    # CARRERAS / DEPORTES
    # --------------------------------------------------------

    "rocketleague": {
        "emoji": "🚗",
        "name": "Rocket League",
        "category": "Carreras",
        "description": "Busca compañeros para Rocket League."
    },

    "forza": {
        "emoji": "🏎️",
        "name": "Forza Horizon",
        "category": "Carreras",
        "description": "Busca gente para conducir en Forza."
    },

    "fc": {
        "emoji": "⚽",
        "name": "EA Sports FC",
        "category": "Deportes",
        "description": "Busca gente para jugar EA Sports FC."
    },

    # --------------------------------------------------------
    # ACCIÓN / RPG
    # --------------------------------------------------------

    "gtav": {
        "emoji": "🚘",
        "name": "GTA V",
        "category": "Acción",
        "description": "Busca gente para jugar GTA V."
    },

    "eldenring": {
        "emoji": "⚔️",
        "name": "Elden Ring",
        "category": "RPG",
        "description": "Busca gente para jugar Elden Ring."
    },

    "baldursgate3": {
        "emoji": "🐉",
        "name": "Baldur's Gate 3",
        "category": "RPG",
        "description": "Busca compañeros para Baldur's Gate 3."
    },

    "genshin": {
        "emoji": "✨",
        "name": "Genshin Impact",
        "category": "RPG",
        "description": "Busca gente para jugar Genshin Impact."
    },

    "warframe": {
        "emoji": "⚔️",
        "name": "Warframe",
        "category": "Acción",
        "description": "Busca compañeros para Warframe."
    },

    "helldivers2": {
        "emoji": "🪖",
        "name": "HELLDIVERS 2",
        "category": "Acción",
        "description": "Busca soldados para defender la galaxia."
    },

    "deadbydaylight": {
        "emoji": "🔪",
        "name": "Dead by Daylight",
        "category": "Terror",
        "description": "Busca supervivientes para Dead by Daylight."
    }
}


# ============================================================
# CONFIGURACIÓN
# ============================================================

MAX_JUGADORES = 5
BUSQUEDAS = {}


# ============================================================
# EMBED DE BÚSQUEDA
# ============================================================

def crear_embed(busqueda):

    datos = GAMES[busqueda["juego"]]
    jugadores = busqueda["jugadores"]

    lista_jugadores = "\n".join(
        f"• {jugador.mention}"
        for jugador in jugadores
    )

    embed = discord.Embed(
        title=f"{datos['emoji']} Buscando jugadores",
        description=(
            f"👤 **{busqueda['organizador'].display_name}** "
            f"está buscando gente para jugar a "
            f"**{datos['name']}**.\n\n"
            "Pulsa **🙋 Unirme** si quieres participar."
        ),
        color=discord.Color.purple()
    )

    embed.add_field(
        name="🎮 Juego",
        value=f"{datos['emoji']} {datos['name']}",
        inline=True
    )

    embed.add_field(
        name="📂 Categoría",
        value=datos["category"],
        inline=True
    )

    embed.add_field(
        name="👥 Jugadores",
        value=f"{len(jugadores)}/{MAX_JUGADORES}",
        inline=True
    )

    embed.add_field(
        name="🧑‍🤝‍🧑 Grupo",
        value=lista_jugadores or "Nadie se ha unido todavía.",
        inline=False
    )

    embed.set_footer(
        text="Foxy Juega Contigo 🦊"
    )

    return embed


# ============================================================
# BOTONES DE LA BÚSQUEDA
# ============================================================

class BusquedaView(discord.ui.View):

    def __init__(self, message_id):

        super().__init__(timeout=None)

        self.message_id = message_id

    @discord.ui.button(
        label="Unirme",
        emoji="🙋",
        style=discord.ButtonStyle.success
    )
    async def unirme(self, interaction, button):

        busqueda = BUSQUEDAS.get(self.message_id)

        if busqueda is None:
            await interaction.response.send_message(
                "❌ Esta búsqueda ya no está activa.",
                ephemeral=True
            )
            return

        jugadores = busqueda["jugadores"]

        if any(
            jugador.id == interaction.user.id
            for jugador in jugadores
        ):
            await interaction.response.send_message(
                "⚠️ Ya estás dentro de esta búsqueda.",
                ephemeral=True
            )
            return

        if len(jugadores) >= MAX_JUGADORES:
            await interaction.response.send_message(
                "❌ Esta búsqueda ya está llena.",
                ephemeral=True
            )
            return

        jugadores.append(interaction.user)

        await interaction.response.edit_message(
            embed=crear_embed(busqueda),
            view=self
        )

    @discord.ui.button(
        label="Salir",
        emoji="🚪",
        style=discord.ButtonStyle.secondary
    )
    async def salir(self, interaction, button):

        busqueda = BUSQUEDAS.get(self.message_id)

        if busqueda is None:
            await interaction.response.send_message(
                "❌ Esta búsqueda ya no está activa.",
                ephemeral=True
            )
            return

        jugadores = busqueda["jugadores"]

        jugador = next(
            (
                jugador
                for jugador in jugadores
                if jugador.id == interaction.user.id
            ),
            None
        )

        if jugador is None:
            await interaction.response.send_message(
                "⚠️ No estás dentro de esta búsqueda.",
                ephemeral=True
            )
            return

        if interaction.user.id == busqueda["organizador"].id:
            await interaction.response.send_message(
                "⚠️ Eres el organizador. "
                "Pulsa **🛑 Cerrar** para terminar la búsqueda.",
                ephemeral=True
            )
            return

        jugadores.remove(jugador)

        await interaction.response.edit_message(
            embed=crear_embed(busqueda),
            view=self
        )

    @discord.ui.button(
        label="Cerrar",
        emoji="🛑",
        style=discord.ButtonStyle.danger
    )
    async def cerrar(self, interaction, button):

        busqueda = BUSQUEDAS.get(self.message_id)

        if busqueda is None:
            await interaction.response.send_message(
                "❌ Esta búsqueda ya está cerrada.",
                ephemeral=True
            )
            return

        if interaction.user.id != busqueda["organizador"].id:
            await interaction.response.send_message(
                "❌ Solo el organizador puede cerrar la búsqueda.",
                ephemeral=True
            )
            return

        del BUSQUEDAS[self.message_id]

        datos = GAMES[busqueda["juego"]]

        embed = discord.Embed(
            title=f"{datos['emoji']} Búsqueda cerrada",
            description=(
                f"La búsqueda de **{datos['name']}** "
                f"ha sido cerrada por "
                f"{interaction.user.mention}."
            ),
            color=discord.Color.red()
        )

        await interaction.response.edit_message(
            embed=embed,
            view=None
        )


# ============================================================
# MENÚ DE SELECCIÓN
# ============================================================

class ElegirJuegoView(discord.ui.View):

    def __init__(self, autor_id):

        super().__init__(timeout=60)

        self.autor_id = autor_id

    async def crear_busqueda(self, interaction, juego):

        if interaction.user.id != self.autor_id:
            await interaction.response.send_message(
                "❌ Solo quien creó el menú puede elegir el juego.",
                ephemeral=True
            )
            return

        for busqueda in BUSQUEDAS.values():

            if busqueda["organizador"].id == interaction.user.id:
                await interaction.response.send_message(
                    "⚠️ Ya tienes una búsqueda activa. "
                    "Cierra la anterior antes de crear otra.",
                    ephemeral=True
                )
                return

        busqueda = {
            "juego": juego,
            "organizador": interaction.user,
            "jugadores": [interaction.user]
        }

        await interaction.response.edit_message(
            content="🎮 Creando búsqueda...",
            embed=None,
            view=None
        )

        mensaje = interaction.message

        BUSQUEDAS[mensaje.id] = busqueda

        view = BusquedaView(mensaje.id)

        await mensaje.edit(
            content=None,
            embed=crear_embed(busqueda),
            view=view
        )

    # --------------------------------------------------------
    # FILA 0
    # --------------------------------------------------------

    @discord.ui.button(
        label="Minecraft",
        emoji="⛏️",
        style=discord.ButtonStyle.primary,
        row=0
    )
    async def minecraft(self, interaction, button):
        await self.crear_busqueda(interaction, "minecraft")

    @discord.ui.button(
        label="R.E.P.O.",
        emoji="👻",
        style=discord.ButtonStyle.danger,
        row=0
    )
    async def repo(self, interaction, button):
        await self.crear_busqueda(interaction, "repo")

    @discord.ui.button(
        label="PEAK",
        emoji="🏔️",
        style=discord.ButtonStyle.success,
        row=0
    )
    async def peak(self, interaction, button):
        await self.crear_busqueda(interaction, "peak")

    @discord.ui.button(
        label="Among Us",
        emoji="🔪",
        style=discord.ButtonStyle.primary,
        row=0
    )
    async def amongus(self, interaction, button):
        await self.crear_busqueda(interaction, "amongus")

    @discord.ui.button(
        label="Valorant",
        emoji="🎯",
        style=discord.ButtonStyle.primary,
        row=0
    )
    async def valorant(self, interaction, button):
        await self.crear_busqueda(interaction, "valorant")

    # --------------------------------------------------------
    # FILA 1
    # --------------------------------------------------------

    @discord.ui.button(
        label="Marvel Rivals",
        emoji="🦸",
        style=discord.ButtonStyle.primary,
        row=1
    )
    async def marvelrivals(self, interaction, button):
        await self.crear_busqueda(interaction, "marvelrivals")

    @discord.ui.button(
        label="DBD",
        emoji="🔪",
        style=discord.ButtonStyle.danger,
        row=1
    )
    async def deadbydaylight(self, interaction, button):
        await self.crear_busqueda(interaction, "deadbydaylight")

    @discord.ui.button(
        label="Roblox",
        emoji="🧱",
        style=discord.ButtonStyle.primary,
        row=1
    )
    async def roblox(self, interaction, button):
        await self.crear_busqueda(interaction, "roblox")

    @discord.ui.button(
        label="Delta Force",
        emoji="🎖️",
        style=discord.ButtonStyle.primary,
        row=1
    )
    async def deltaforce(self, interaction, button):
        await self.crear_busqueda(interaction, "deltaforce")

    @discord.ui.button(
        label="Fortnite",
        emoji="🔫",
        style=discord.ButtonStyle.primary,
        row=1
    )
    async def fortnite(self, interaction, button):
        await self.crear_busqueda(interaction, "fortnite")


# ============================================================
# COMANDO !JUGAR
# ============================================================

@commands.command(name="jugar")
async def jugar(ctx):

    embed = discord.Embed(
        title="🎮 Foxy Juega Contigo",
        description=(
            "🦊 ¡Busca gente de la comunidad para jugar!\n\n"
            f"Actualmente tenemos **{len(GAMES)} juegos** disponibles.\n\n"
            "Usa `!buscargente` para buscar jugadores."
        ),
        color=discord.Color.purple()
    )

    categorias = {}

    for juego in GAMES.values():

        categorias.setdefault(
            juego["category"],
            []
        ).append(
            f"{juego['emoji']} {juego['name']}"
        )

    for categoria, juegos in categorias.items():

        embed.add_field(
            name=f"📂 {categoria}",
            value=" • ".join(juegos),
            inline=False
        )

    embed.set_footer(
        text="Foxy Juega Contigo 🦊"
    )

    await ctx.send(embed=embed)


# ============================================================
# COMANDO !BUSCARGENTE
# ============================================================

@commands.command(name="buscargente")
async def buscargente(ctx, *, juego=None):

    # --------------------------------------------------------
    # SIN JUEGO -> MOSTRAR BOTONES
    # --------------------------------------------------------

    if juego is None:

        embed = discord.Embed(
            title="🎮 Busca jugadores",
            description=(
                "🦊 **¿A qué quieres jugar?**\n\n"
                "Elige uno de los juegos:"
            ),
            color=discord.Color.purple()
        )

        embed.add_field(
            name="🔥 Juegos",
            value=(
                "⛏️ Minecraft\n"
                "👻 R.E.P.O.\n"
                "🏔️ PEAK\n"
                "🔪 Among Us 🔴\n"
                "🎯 Valorant\n"
                "🦸 Marvel Rivals\n"
                "🔪 Dead by Daylight\n"
                "🧱 Roblox\n"
                "🎖️ Delta Force\n"
                "🔫 Fortnite"
            ),
            inline=False
        )

        embed.add_field(
            name="📚 Más juegos",
            value=(
                f"Tenemos **{len(GAMES)} juegos** disponibles.\n\n"
                "También puedes escribir directamente:\n"
                "`!buscargente minecraft`"
            ),
            inline=False
        )

        embed.set_footer(
            text="Tienes 60 segundos para elegir."
        )

        await ctx.send(
            embed=embed,
            view=ElegirJuegoView(ctx.author.id)
        )

        return

    # --------------------------------------------------------
    # BUSCAR JUEGO POR NOMBRE
    # --------------------------------------------------------

    juego = juego.lower().strip()

    if juego not in GAMES:

        encontrado = None

        for clave, datos in GAMES.items():

            if juego == datos["name"].lower():
                encontrado = clave
                break

        if encontrado is not None:

            juego = encontrado

        else:

            disponibles = ", ".join(
                datos["name"]
                for datos in GAMES.values()
            )

            await ctx.send(
                "❌ No conozco ese juego.\n\n"
                f"🎮 Juegos disponibles:\n{disponibles}"
            )

            return

    # --------------------------------------------------------
    # COMPROBAR BÚSQUEDA ACTIVA
    # --------------------------------------------------------

    for busqueda in BUSQUEDAS.values():

        if busqueda["organizador"].id == ctx.author.id:

            await ctx.send(
                "⚠️ Ya tienes una búsqueda activa.\n"
                "Cierra la anterior antes de crear otra."
            )

            return

    # --------------------------------------------------------
    # CREAR BÚSQUEDA
    # --------------------------------------------------------

    busqueda = {
        "juego": juego,
        "organizador": ctx.author,
        "jugadores": [ctx.author]
    }

    mensaje = await ctx.send(
        "🎮 Creando búsqueda..."
    )

    BUSQUEDAS[mensaje.id] = busqueda

    view = BusquedaView(mensaje.id)

    await mensaje.edit(
        content=None,
        embed=crear_embed(busqueda),
        view=view
    )


# ============================================================
# MINI JUEGO
# ============================================================

@commands.command(name="jueguito")
async def jueguito(ctx):

    opciones = [
        "🎲 Jugar a los dados",
        "🪙 Jugar a cara o cruz",
        "✊ Jugar a piedra, papel o tijera",
        "🎯 Elegir un número aleatorio"
    ]

    await ctx.send(
        f"🦊 **Foxy ha elegido:** "
        f"{random.choice(opciones)}"
    )


# ============================================================
# CARGAR SISTEMA
# ============================================================

def setup_games(bot):

    bot.add_command(jugar)
    bot.add_command(buscargente)
    bot.add_command(jueguito)

    print("🎮 Sistema de juegos cargado")