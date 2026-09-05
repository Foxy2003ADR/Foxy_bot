import os

import discord
from dotenv import load_dotenv


load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

print("TOKEN CARGADO:", bool(TOKEN))
print("LONGITUD:", len(TOKEN) if TOKEN else 0)

if not TOKEN:
    raise RuntimeError("No se encontró DISCORD_TOKEN.")


intents = discord.Intents.none()
intents.guilds = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"LOGIN CORRECTO: {client.user}")
    await client.close()


try:
    client.run(TOKEN)

except discord.LoginFailure as error:
    print("LOGIN FALLIDO")
    print("Detalle:", error)

except Exception as error:
    print("ERROR:")
    print(error)