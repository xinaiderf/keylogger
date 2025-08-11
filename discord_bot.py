import discord
from discord.ext import commands
from discord.utils import get
import asyncio
from dotenv import load_dotenv
import os
from funcoes import identificar_usuario, criar_canal

load_dotenv()

TOKEN = os.getenv('token_dc')
GUILD_ID = int(os.getenv('guild_id'))
CHANNEL_NAME = identificar_usuario()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)
target_channel = None
message_queue = asyncio.Queue()

@bot.event
async def on_ready():
    global target_channel, CHANNEL_NAME
    print(f"Bot conectado como {bot.user}")

    guild = get(bot.guilds, id=GUILD_ID)
    if not guild:
        print(f"Guilda com ID {GUILD_ID} não encontrada.")
        return

    target_channel = get(guild.text_channels, name=CHANNEL_NAME)
    if target_channel:
        print(f"Canal encontrado: {target_channel.name}")
    else:
        print(f"Canal '{CHANNEL_NAME}' não encontrado na guilda '{guild.name}'. Tentando criar...")
        loop = asyncio.get_running_loop()
        # Criar canal sem travar o bot
        await loop.run_in_executor(None, criar_canal)
        # Atualiza referência do canal criado
        target_channel = get(guild.text_channels, name=CHANNEL_NAME)
        if target_channel:
            print(f"Canal criado e encontrado: {target_channel.name}")
        else:
            print("Falha ao encontrar canal após criação.")

    # Inicia task para enviar mensagens da fila
    bot.loop.create_task(message_sender())

async def message_sender():
    while True:
        texto = await message_queue.get()
        if target_channel:
            try:
                await target_channel.send(texto)
            except Exception as e:
                print(f"Erro ao enviar mensagem: {e}")
        else:
            print("Canal para envio não definido.")
        message_queue.task_done()

async def send_message(texto: str):
    await message_queue.put(texto)

def start_bot():
    bot.run(TOKEN)
