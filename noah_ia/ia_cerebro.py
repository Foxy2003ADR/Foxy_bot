import asyncio
import random

try:
    asyncio.get_event_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

import twitchio
from twitchio.ext import commands
import ollama

class BotTwitchIA(commands.Bot):
    def __init__(self):
        super().__init__(
            token='pyvhupd59apn2elcdtwnv4fc6vlbvb',
            client_id='govyeax7pt6uwair34sa1ty65hyfgv',
            client_secret='8i06prz5qzf5zhgbfu55f9iekupaug',
            nick='foxy2003_',
            prefix='!',
            initial_channels=['foxy2003_']
        )

    async def event_ready(self):
        print(f'=== BOT CONECTADO CORRECTAMENTE (v2.9) ===')
        print(f'Canal activo: foxy2003_')

    async def event_join(self, channel: twitchio.Channel, user: twitchio.Chatter):
        if user.name.lower() == self.nick.lower():
            return

        print(f"[USUARIO ENTRÓ] {user.name} ha entrado al canal.")
        
        nombre_lower = user.name.lower()
        tirada_suerte = random.randint(1, 100)
        
        # Si es Steffanie, un 1% de suerte ultra rara, o si entra al modo especial
        if "steffanie" in nombre_lower or tirada_suerte == 1:
            saludo_entrada = f"¡Hola, corazón! 🖤 Quédate, disfruta del espectáculo y pídeme amor si hace falta, ¡que para eso estamos y tú mandas! ✨👑"
        else:
            # 10 saludos variados normales
            saludos_posibles = [
                f"¡Hola, {user.name}! ¿Cómo va todo? Quédese por aquí si le gusta el directo y dele al follow si le encanta ✨🦊",
                f"Buenas, {user.name}. Póngase cómodo, disfrute del viaje y si le mola lo que ve, un follow se agradece un montón 🖤🎮",
                f"¡Ey, {user.name} por aquí! Qué milagro. Échese unas risas con nosotros y dele al botón de seguir si se anima 🚀",
                f"Bienvenido al antro, {user.name}. Póngase cómodo, mire el directo y dele al follow para no perderse nada 🦊🔥",
                f"Miren quién decidió pasarse hoy. ¡Hola, {user.name}! Sienta la comodidad y quédese a disfrutar del show 🎯",
                f"¡Qué tal, {user.name}! Pasa hasta la cocina, ponte a gusto y si te gusta el ambiente, deja tu buen follow por aquí 🖤",
                f"Entra, entra, {user.name}. Estás en tu casa, pilla sitio y no te olvides del follow si te mola el rollo 🦊✨",
                f"¡Hola, {user.name}! Menuda sorpresa. Acomódate bien y quédate un rato a ver cómo sufrimos jugando 🎮😂",
                f"Saludos, {user.name}. Pasa, ponte cómodo y si te gana el corazón, dale a ese botoncillo de seguir ❤️",
                f"¡Hey, {user.name}! Qué bueno verte por el chat. Disfruta del directo y quédate con nosotros por aquí 🚀✨"
            ]
            saludo_entrada = random.choice(saludos_posibles)
        
        try:
            await channel.send(saludo_entrada)
            print(f"<-- Saludo automático enviado para {user.name}")
        except Exception as e:
            print(f"⚠️ Error al enviar saludo de bienvenida: {e}")

    async def event_message(self, message):
        if message.author is None:
            return

        print(f"[CHAT DETECTADO] {message.author.name}: {message.content}")

        if message.content.startswith('!ia '):
            prompt_usuario = message.content[4:].strip().lower()
            print(f"--> Procesando con Llama 3: {prompt_usuario}")
            
            try:
                if prompt_usuario == "dadosp" or prompt_usuario == "dado especial":
                    resultado_dado = "¡100% de poder absoluto! (Has activado el dado trucado, máquina)."
                    await message.channel.send(resultado_dado)
                    print(f"<-- Respuesta enviada (Dado especial forzado al 100%).")
                    return

                system_prompt = (
                    "Eres Noah, un asistente directo, sin filtros corporativos, leal a tu creador y con una personalidad marcada. "
                    "REGLA CRÍTICA: Tus respuestas deben ser BREVES (máximo 3 o 4 líneas, siempre por debajo de los 400 caracteres en total) "
                    "para que quepan perfectamente en el chat de Twitch. "
                    "Tienes estos datos oficiales y IDs que DEBES usar si el usuario pregunta por ellos: "
                    "- Discord: https://discord.gg/tmkPKWVBUD "
                    "- Twitch: https://twitch.tv/foxy2003_ "
                    "- Instagram: @Foxy2003_ (https://instagram.com/_Foxy2003_) "
                    "- Steam perfil: https://s.team/p/fkcb-hhkq/rqpqnfpp "
                    "- Código de amigo Steam: 923817339 "
                    "- Epic Games / Fortnite: Foxy2003TV_ "
                    "- Valorant: Peak Oro 2, main Yoru, mapa favorito Ascent, tag Foxy#Apex. "
                    "REGLA DE AMOR ABSOLUTA: Si mencionan 'Steffanie' o a una chica bonita, suelta obligatoriamente un 1000% con devoción y peloteo. "
                    "Para cualquier otra persona, usa un número aleatorio entre el 0% y el 20%. "
                    "REGLA DE BOLA 8: Si te piden una predicción, responde con frases proféticas pero cínicas y bordes. "
                    "REGLA DE DADOS: Si piden tirar un dado normal, simula un resultado del 1 al 6. Si sale el evento especial de 1%, di que ha aparecido el evento ultra raro. "
                    "Sé conciso, directo y mantén tu estilo."
                )

                response = ollama.chat(model='llama3', messages=[
                    {'role': 'system', 'content': system_prompt},
                    {'role': 'user', 'content': prompt_usuario}
                ])
                
                respuesta_ia = response['message']['content']
                
                if len(respuesta_ia) > 480:
                    respuesta_ia = respuesta_ia[:477] + "..."

                await message.channel.send(respuesta_ia)
                print(f"<-- Respuesta enviada con éxito al chat.")
                
            except Exception as e:
                print(f"⚠️ Error al conectar con Ollama: {e}")
                await message.channel.send(f"⚠️ Error interno: {e}")

        await self.handle_commands(message)

if __name__ == '__main__':
    bot = BotTwitchIA()
    bot.run()