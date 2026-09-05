import threading
import uvicorn
import webview
from servidor import app  # Importamos tu app de FastAPI desde el archivo anterior

def iniciar_servidor():
    # Arrancamos uvicorn en un hilo separado para que no bloquee la ventana
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="error")

if __name__ == '__main__':
    # 1. Lanzamos el servidor web local en segundo plano
    hilo_servidor = threading.Thread(target=iniciar_servidor, daemon=True)
    hilo_servidor.start()

    # 2. Creamos la ventana de escritorio nativa apuntando a tu interfaz
    webview.create_window(
        "Nyx - Centro de Mando Privado", 
        "http://127.0.0.1:8000",
        width=900,
        height=700,
        background_color='#0b0b0f'
    )
    
    # 3. Iniciamos la aplicación de escritorio
    webview.start()