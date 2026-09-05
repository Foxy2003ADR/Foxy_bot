import asyncio
import os
import uuid

import edge_tts


VOICE = "es-ES-AlvaroNeural"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_DIR = os.path.join(BASE_DIR, "temp")

os.makedirs(TEMP_DIR, exist_ok=True)


async def generar_voz(texto: str) -> str:
    """
    Genera el audio TTS en español usando
    la voz masculina de Microsoft Edge TTS.
    """

    nombre = f"tts_{uuid.uuid4().hex}.mp3"
    salida = os.path.join(TEMP_DIR, nombre)

    communicate = edge_tts.Communicate(
        texto,
        VOICE
    )

    await communicate.save(salida)

    return salida


async def generar_voz_animatronica(texto: str) -> tuple[str, str]:
    """
    Genera la voz y después aplica el efecto
    animatrónico mediante FFmpeg.

    Devuelve:
        (archivo_original, archivo_procesado)
    """

    original = await generar_voz(texto)

    procesado = os.path.join(
        TEMP_DIR,
        f"foxy_{uuid.uuid4().hex}.mp3"
    )

    comando = [
        "ffmpeg",
        "-y",
        "-i",
        original,
        "-af",
        (
            "rubberband=pitch=0.82,"
            "acompressor=threshold=-18dB:ratio=3:attack=10:release=100,"
            "acrusher=bits=12:mix=0.08,"
            "highpass=f=75,"
            "lowpass=f=10000"
        ),
        procesado
    ]

    proceso = await asyncio.create_subprocess_exec(
        *comando,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    stdout, stderr = await proceso.communicate()

    if proceso.returncode != 0:
        try:
            os.remove(original)
        except OSError:
            pass

        error = stderr.decode(errors="ignore")

        raise RuntimeError(
            f"FFmpeg no pudo procesar el audio:\n{error}"
        )

    return original, procesado


def borrar_archivo(ruta: str):
    """
    Borra un archivo si existe.
    """

    try:
        if ruta and os.path.exists(ruta):
            os.remove(ruta)
    except OSError:
        pass