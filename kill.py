from fastapi import FastAPI, HTTPException, Header
import os
from dotenv import load_dotenv
import requests
import sys
import subprocess
from funcoes import identificar_usuario, send

app = FastAPI()
load_dotenv()


## VARIAVEIS ##
secret_token = os.getenv('SECRET_TOKEN')
url = os.getenv('webhook_url_hhh')
diretorio_arquivo = os.path.dirname(__file__)


# Identificação do usuario 
user_identification = identificar_usuario()

# Função para enviar notificações

def kill():
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


# Cria uma rota com a identificação do usuario para deletar somente esse usuario
@app.post(f'/destruir/{user_identification}')
def destruir(token: str = Header(...)):
    if token != secret_token:
        raise HTTPException(status_code=403, detail='ACESSO NEGADO MEU PATRÃO RSRS')

    kill()


# Rota de Delete All 
@app.post('/kill-all')
def kill_all(token: str = Header(...)):
    if token != secret_token:
        raise HTTPException(status_code=403, detail='ACESSO NEGADO MEU PATRÃO RSRS')
    
    kill()