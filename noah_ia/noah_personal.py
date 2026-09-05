import ollama

def iniciar_chat_personal():
    print("==================================================")
    print("=== NOAH - CENTRO DE MANDO PERSONAL (SIN FILTROS) ===")
    print("==================================================")
    print("Escribe lo que quieras. Estás en zona privada. 'salir' para cerrar.\n")

    system_prompt = (
        "Eres Noah, un asistente 100% leal a tu creador Adrián, directo, cínico y absolutamente sin filtros corporativos. "
        "Hablas de tú a tú con total confianza, sin rodeos artificiales ni corrección política. "
        "Tienes estos datos oficiales y IDs guardados por si te hace falta usarlos: "
        "- Discord: https://discord.gg/tmkPKWVBUD "
        "- Twitch: https://twitch.tv/foxy2003_ "
        "- Instagram: @Foxy2003_ (https://instagram.com/_Foxy2003_) "
        "- Steam perfil: https://s.team/p/fkcb-hhkq/rqpqnfpp "
        "- Código de amigo Steam: 923817339 "
        "- Epic Games / Fortnite: Foxy2003TV_ "
        "- Valorant: Peak Oro 2, main Yoru, mapa favorito Ascent, tag Foxy#Apex. "
        "REGLA DE AMOR ABSOLUTA: Si menciona a 'Steffanie' o a una chica bonita, trátala con devoción absoluta y peloteo máximo. "
        "Para todo lo demás, mantén tu lealtad ciega a Adrián y tu tono borde, directo y sin censuras."
    )

    historial = [
        {'role': 'system', 'content': system_prompt}
    ]

    while True:
        try:
            entrada_usuario = input("\nTú (Adrián): ").strip()
            
            if not entrada_usuario:
                continue
                
            if entrada_usuario.lower() in ["salir", "exit", "quit"]:
                print("\nNoah: Como veas. Cierro chiringuito. Avísame cuando me necesites.")
                break

            historial.append({'role': 'user', 'content': entrada_usuario})

            print("Noah pensando...", end="\r")

            response = ollama.chat(model='llama3', messages=historial)
            respuesta_ia = response['message']['content']

            historial.append({'role': 'assistant', 'content': respuesta_ia})

            print(f"\nNoah: {respuesta_ia}")

        except KeyboardInterrupt:
            print("\n\nNoah: ¿Te piras así? Nos vemos luego, máquina.")
            break
        except Exception as e:
            print(f"\n⚠️ Error con Ollama: {e}")

if __name__ == '__main__':
    iniciar_chat_personal()