import asyncio
import discord


TIEMPO_SALIDA = 60

tareas_salida = {}


def hay_usuarios_en_canal(canal: discord.VoiceChannel) -> bool:
    return any(
        not miembro.bot
        for miembro in canal.members
    )


async def desconectar_si_vacio(
    bot,
    guild_id: int,
    canal_id: int
):
    clave = (guild_id, canal_id)

    try:
        await asyncio.sleep(TIEMPO_SALIDA)

        guild = bot.get_guild(guild_id)

        if guild is None:
            return

        canal = guild.get_channel(canal_id)

        if canal is None:
            return

        voice_client = guild.voice_client

        if voice_client is None:
            return

        if voice_client.channel is None:
            return

        if voice_client.channel.id != canal_id:
            return

        if hay_usuarios_en_canal(canal):
            return

        if voice_client.is_playing():
            voice_client.stop()

        await voice_client.disconnect()

        print(
            f"🔊 Foxy salió de {canal.name} "
            f"por inactividad."
        )

    except asyncio.CancelledError:
        pass

    except Exception as error:
        print(
            f"❌ Error en Voice Auto: {error}"
        )

    finally:
        tarea = tareas_salida.get(clave)

        if tarea is asyncio.current_task():
            tareas_salida.pop(clave, None)


def cancelar_salida(
    guild_id: int,
    canal_id: int
):
    clave = (guild_id, canal_id)

    tarea = tareas_salida.pop(
        clave,
        None
    )

    if tarea is not None:
        tarea.cancel()


def programar_salida(
    bot,
    guild_id: int,
    canal_id: int
):
    cancelar_salida(
        guild_id,
        canal_id
    )

    tarea = asyncio.create_task(
        desconectar_si_vacio(
            bot,
            guild_id,
            canal_id
        )
    )

    tareas_salida[
        (guild_id, canal_id)
    ] = tarea


def setup_voice_auto(bot):

    @bot.listen("on_voice_state_update")
    async def voice_auto_update(
        miembro: discord.Member,
        antes: discord.VoiceState,
        despues: discord.VoiceState
    ):
        if miembro.bot:
            return

        guild = miembro.guild

        # --------------------------------
        # SALIDA DEL CANAL ANTERIOR
        # --------------------------------

        if antes.channel is not None:

            canal_anterior = antes.channel

            voice_client = guild.voice_client

            if (
                voice_client is not None
                and voice_client.channel is not None
                and voice_client.channel.id
                == canal_anterior.id
            ):
                if not hay_usuarios_en_canal(
                    canal_anterior
                ):
                    programar_salida(
                        bot,
                        guild.id,
                        canal_anterior.id
                    )

        # --------------------------------
        # ENTRADA AL NUEVO CANAL
        # --------------------------------

        if despues.channel is None:
            return

        canal_nuevo = despues.channel

        cancelar_salida(
            guild.id,
            canal_nuevo.id
        )

        voice_client = guild.voice_client

        # Foxy ya está conectado aquí
        if (
            voice_client is not None
            and voice_client.channel is not None
            and voice_client.channel.id
            == canal_nuevo.id
        ):
            return

        # Foxy está conectado en otro canal.
        # No lo movemos automáticamente.
        if voice_client is not None:
            return

        try:
            await canal_nuevo.connect(
                self_deaf=True
            )

            print(
                f"🔊 Foxy entró automáticamente "
                f"en {canal_nuevo.name}."
            )

        except discord.ClientException:
            pass

        except discord.Forbidden:
            print(
                f"❌ Foxy no tiene permisos "
                f"para entrar en {canal_nuevo.name}."
            )

        except Exception as error:
            print(
                f"❌ Error entrando al canal de voz: "
                f"{error}"
            )