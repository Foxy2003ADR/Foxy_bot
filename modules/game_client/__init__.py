from discord.ext import commands

from .manager import GameClientManager
from .adapters.demo import DemoAdapter


game_manager = GameClientManager()


def setup_game_client(bot: commands.Bot):

    game_manager.register(
        "demo",
        DemoAdapter
    )

    @bot.group(
        name="juego",
        invoke_without_command=True
    )
    async def juego(ctx):
        await ctx.send(
            "🎮 **Game Client de Foxy**\n\n"
            "Usa `!juego ayuda` para ver los comandos."
        )

    @juego.command(name="ayuda")
    async def juego_ayuda(ctx):
        await ctx.send(
            "🎮 **Comandos Game Client**\n\n"
            "`!juego lista`\n"
            "`!juego conectar demo`\n"
            "`!juego estado`\n"
            "`!juego mover <direccion>`\n"
            "`!juego hablar <mensaje>`\n"
            "`!juego interactuar`\n"
            "`!juego desconectar`"
        )

    @juego.command(name="lista")
    async def juego_lista(ctx):
        juegos = game_manager.available_games()

        if not juegos:
            await ctx.send("❌ No hay juegos registrados.")
            return

        texto = "\n".join(
            f"🎮 `{juego}`"
            for juego in juegos
        )

        await ctx.send(
            f"🎮 **Juegos disponibles:**\n\n{texto}"
        )

    @juego.command(name="conectar")
    async def juego_conectar(ctx, juego: str):
        try:
            client = await game_manager.connect(
                user_id=ctx.author.id,
                game=juego,
                player_name="Foxy"
            )

            await ctx.send(
                f"🦊 **Foxy conectado**\n\n"
                f"🎮 Juego: `{client.game_name}`\n"
                f"👤 Personaje: `{client.state.player_name}`"
            )

        except ValueError as e:
            await ctx.send(f"❌ {e}")

        except Exception as e:
            await ctx.send(
                f"❌ Error conectando a `{juego}`:\n"
                f"`{type(e).__name__}: {e}`"
            )

    @juego.command(name="desconectar")
    async def juego_desconectar(ctx):
        disconnected = await game_manager.disconnect(
            ctx.author.id
        )

        if not disconnected:
            await ctx.send(
                "❌ Foxy no está conectado a ningún juego."
            )
            return

        await ctx.send(
            "🔌 🦊 Foxy se ha desconectado del juego."
        )

    @juego.command(name="estado")
    async def juego_estado(ctx):
        state = await game_manager.get_state(
            ctx.author.id
        )

        if state is None:
            await ctx.send(
                "❌ Foxy no está conectado a ningún juego."
            )
            return

        posicion = (
            f"({state.x}, {state.y})"
            if state.x is not None and state.y is not None
            else "desconocida"
        )

        vida = (
            f"{state.hp}/{state.max_hp}"
            if state.hp is not None and state.max_hp is not None
            else "desconocida"
        )

        await ctx.send(
            "🎮 **Estado de Foxy**\n\n"
            f"Juego: `{state.game}`\n"
            f"Conectado: `{'Sí' if state.connected else 'No'}`\n"
            f"En partida: `{'Sí' if state.in_game else 'No'}`\n"
            f"Personaje: `{state.player_name}`\n"
            f"❤️ Vida: `{vida}`\n"
            f"📍 Posición: `{posicion}`"
        )

    @juego.command(name="mover")
    async def juego_mover(ctx, direccion: str):
        client = game_manager.get_client(ctx.author.id)

        if client is None or not client.state.connected:
            await ctx.send(
                "❌ Foxy no está conectado a ningún juego."
            )
            return

        try:
            state = await client.move(direccion)

            await ctx.send(
                f"🦊 Foxy se mueve hacia **{direccion}**.\n"
                f"📍 Posición: `{state.x}, {state.y}`"
            )

        except Exception as e:
            await ctx.send(
                f"❌ Error moviendo a Foxy: `{e}`"
            )

    @juego.command(name="hablar")
    async def juego_hablar(ctx, *, mensaje: str):
        client = game_manager.get_client(ctx.author.id)

        if client is None or not client.state.connected:
            await ctx.send(
                "❌ Foxy no está conectado a ningún juego."
            )
            return

        await client.send_chat(mensaje)

        await ctx.send(
            f"💬 Foxy dice:\n> {mensaje}"
        )

    @juego.command(name="interactuar")
    async def juego_interactuar(ctx):
        client = game_manager.get_client(ctx.author.id)

        if client is None or not client.state.connected:
            await ctx.send(
                "❌ Foxy no está conectado a ningún juego."
            )
            return

        await client.interact()

        await ctx.send(
            "🦊 Foxy ha interactuado con el entorno."
        )

    return game_manager