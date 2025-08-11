import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv('token_dc')

intents = discord.Intents.default()  # Intents padrões
intents.message_content = True       # Se quiser receber conteúdo das mensagens (necessário pra ler mensagens)

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logado como {client.user}')

client.run(TOKEN)
