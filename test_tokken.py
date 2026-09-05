import os
import hashlib
import requests
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("DISCORD_TOKEN", "")

print("TOKEN CARGADO:", bool(token))
print("LONGITUD:", len(token))
print("HUELLA:", hashlib.sha256(token.encode()).hexdigest()[:16])

headers = {
    "Authorization": f"Bot {token}"
}

response = requests.get(
    "https://discord.com/api/v10/users/@me",
    headers=headers,
    timeout=10
)

print("HTTP:", response.status_code)
print("RESPUESTA:", response.text)