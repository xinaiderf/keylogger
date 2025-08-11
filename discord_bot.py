import discord
from discord.ext import commands
<<<<<<< HEAD
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
=======

# Coloque aqui o token do seu bot
TOKEN = 'SEU_TOKEN_AQUI'

intents = discord.Intents.default()
intents.message_content = True  # necessário para ler mensagens

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

bot.run(TOKEN)
>>>>>>> c16315cf543b2ef9fad561d828c6027ba7b10767
