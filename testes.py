import discord
from discord import app_commands
import os
from dotenv import load_dotenv
import requests

load_dotenv()
token_dc = os.getenv('token_dc')
secret_token = os.getenv('SECRET_TOKEN')
ip_publico = requests.get('https://httpbin.org/ip').json()['origin']

client = discord.Client(intents=discord.Intents.default())
tree = app_commands.CommandTree(client)

async def alvo_autocomplete(interaction: discord.Interaction, current: str):
    if not interaction.guild:
        return []

    # Lista canais de texto filtrando pelo que o usuário digitou
    canais = [
        app_commands.Choice(name=canal.name, value=str(canal.id))
        for canal in interaction.guild.text_channels
        if current.lower() in canal.name.lower()
    ]
    return canais[:25]  # Discord aceita no máximo 25

@tree.command(name="kill_remote", description="Executa KILL em outro PC")
@app_commands.autocomplete(alvo=alvo_autocomplete)
async def kill_remote(interaction: discord.Interaction, alvo: str):
    url = f"{ip_publico}/destruir/{alvo}"
    headers = {"token": secret_token}

    try:
        r = requests.post(url, headers=headers, timeout=5)
        if r.status_code == 200:
            await interaction.response.send_message(f"KILL enviado para alvo `{alvo}` 💀")
        else:
            await interaction.response.send_message(f"Erro: {r.text}")
    except Exception as e:
        await interaction.response.send_message(f"Falha: {e}")


client.run(token_dc)
