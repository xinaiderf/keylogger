import discord
from discord.ext import commands

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
