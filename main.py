from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import os
import subprocess
from playwright.sync_api import sync_playwright
import sys
import tkinter as tk
import time
#TTS add
import simpleaudio as sa

import speech_recognition as sr
import whisper
import torch
import numpy as np

# Configuration
args = sys.argv[1:]

save_ids = os.path.exists("game_path.txt")

root = tk.Tk()
root.title("MonikA.I. Submod")
root.geometry("400x400")
root.resizable(False, False)

def get_input():
    global USERNAME
    global PASSWORD
    global CHOOSE_CHARACTER
    global GAME_PATH
    global USE_CHARACTER_AI
    global USE_TTS
    global DEBUG_MODE
    USERNAME = username.get()
    PASSWORD = password.get()
    CHOOSE_CHARACTER = choose_character.get()
    USE_CHARACTER_AI = use_character_ai.get()
    USE_TTS = use_tts.get()
    GAME_PATH = game_path.get()
    DEBUG_MODE = debug_mode.get()
    root.destroy()

username = tk.StringVar()
password = tk.StringVar()
choose_character = tk.StringVar()
use_character_ai = tk.StringVar()
use_tts = tk.StringVar()
game_path = tk.StringVar()
debug_mode = tk.StringVar()

# tk.Label(root, text="Username").grid(row=0, column=0)
# tk.Label(root, text="Password").grid(row=1, column=0)
tk.Label(root, text="Choose Character").grid(row=3, column=0)
tk.Label(root, text="Use Character AI").grid(row=5, column=0)
tk.Label(root, text="Use TTS").grid(row=6, column=0)
tk.Label(root, text="Use Debug Mode").grid(row=7, column=0)

# tk.Entry(root, textvariable=username).grid(row=0, column=1)
# tk.Entry(root, textvariable=password, show='*').grid(row=1, column=1)
tk.Entry(root, textvariable=choose_character).grid(row=3, column=1)

tk.Radiobutton(root, text="Yes", variable=use_character_ai, value=True).grid(row=5, column=1)
tk.Radiobutton(root, text="No", variable=use_character_ai, value=False).grid(row=5, column=2)

tk.Radiobutton(root, text="Yes", variable=use_tts, value=True).grid(row=6, column=1)
tk.Radiobutton(root, text="No", variable=use_tts, value=False).grid(row=6, column=2)

tk.Radiobutton(root, text="Yes", variable=debug_mode, value=True).grid(row=7, column=1)
tk.Radiobutton(root, text="No", variable=debug_mode, value=False).grid(row=7, column=2)

tk.Button(root, text="Submit", command=get_input).grid(row=8, column=0)

if save_ids:
    #Make button appear if the previous one was clicked
    def on_select(v):
        global GAME_PATH
        if v == True:            
            tk.Label(root, text="Change Game Path").grid(row=4, column=0)
            tk.Entry(root, textvariable=game_path).grid(row=4, column=3)

            tk.Label(root, text="Change email").grid(row=0, column=0)
            tk.Entry(root, textvariable=username).grid(row=0, column=3)

            tk.Label(root, text="Change password").grid(row=1, column=0)
            tk.Entry(root, textvariable=password,show='*').grid(row=1, column=3)
        else:
            with open("game_path.txt", "r") as f:
                string = f.read()
                GAME_PATH,USERNAME,PASSWORD = string.split(";")
            #Write GAME_PATH in the box
            tk.Label(root, text="Change Game Path").grid(row=4, column=0)
            tk.Entry(root, textvariable=game_path).grid(row=4, column=3)
            game_path.set(GAME_PATH)

            tk.Label(root, text="Change email").grid(row=0, column=0)
            tk.Entry(root, textvariable=username).grid(row=0, column=3)
            username.set(USERNAME)

            tk.Label(root, text="Change password").grid(row=1, column=0)
            tk.Entry(root, textvariable=password,show='*').grid(row=1, column=3)
            password.set(PASSWORD)

    tk.Label(root, text="Change Game Path").grid(row=4, column=0)
    change_game_path = tk.BooleanVar()

    yes_change = tk.Radiobutton(root, text="Yes", variable=change_game_path, value=True)
    yes_change.grid(row=4, column=1)
    yes_change.config(command=lambda: on_select(True))

    no_change = tk.Radiobutton(root, text="No", variable=change_game_path, value=False)
    no_change.grid(row=4, column=2)
    no_change.config(command=lambda: on_select(False))

    tk.Label(root, text="Change email").grid(row=0, column=0)
    change_email = tk.BooleanVar()

    yes_change = tk.Radiobutton(root, text="Yes", variable=change_email, value=True)
    yes_change.grid(row=0, column=1)
    yes_change.config(command=lambda: on_select(True))

    no_change = tk.Radiobutton(root, text="No", variable=change_email, value=False)
    no_change.grid(row=0, column=2)
    no_change.config(command=lambda: on_select(False))

    tk.Label(root, text="Change password").grid(row=1, column=0)
    change_password = tk.BooleanVar()

    yes_change = tk.Radiobutton(root, text="Yes", variable=change_password, value=True)
    yes_change.grid(row=1, column=1)
    yes_change.config(command=lambda: on_select(True))

    no_change = tk.Radiobutton(root, text="No", variable=change_password, value=False)
    no_change.grid(row=1, column=2)
    no_change.config(command=lambda: on_select(False))

else:
    game_path = tk.StringVar()
    tk.Label(root, text="Game Path").grid(row=4, column=0)
    tk.Entry(root, textvariable=game_path).grid(row=4, column=1)

    username = tk.StringVar()
    tk.Label(root, text="Email").grid(row=0, column=0)
    tk.Entry(root, textvariable=username).grid(row=0, column=1)

    password = tk.StringVar()
    tk.Label(root, text="Password").grid(row=1, column=0)
    tk.Entry(root, textvariable=password, show='*').grid(row=1, column=1)
    
root.mainloop()

#Write game_path to a file
if GAME_PATH != "" and USERNAME != "" and PASSWORD != "":
    with open("game_path.txt", "w") as f:
        f.write(GAME_PATH + ";" + USERNAME + ";" + PASSWORD)

characters_pages = {
    "0": '[href="/chat?char=e9UVQuLURpLyCdhi8OjSKSLwKIiE0U-nEqXDeAjk538"]',
    "1": '[href="/chat?char=EdSSlsl49k3wnwvMvK4eCh4yOFBaGTMJ7Q9CxtG2DiU"]'
}

USE_TTS = int(USE_TTS)
USE_CHARACTER_AI = int(USE_CHARACTER_AI)
DEBUG_MODE = int(DEBUG_MODE)

#Convert GAME_PATH to Linux format
GAME_PATH = GAME_PATH.replace("\\", "/")
# Global variables 
clients = {}
addresses = {}
HOST = '127.0.0.1'
PORT = 12346
BUFSIZE = 1024
ADDRESS = (HOST, PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDRESS)

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

####Load the speech recognizer#####
english = True
def init_stt(model="base", english=True,energy=300, pause=0.8, dynamic_energy=False):
    if model != "large" and english:
        model = model + ".en"
    audio_model = whisper.load_model(model)    
    
    #load the speech recognizer and set the initial energy threshold and pause threshold
    r = sr.Recognizer()
    r.energy_threshold = energy
    r.pause_threshold = pause
    r.dynamic_energy_threshold = dynamic_energy

    return r,audio_model

r,audio_model = init_stt()

def listen():
	""" Wait for incoming connections """
	print("Waiting for connection...")
	while True:
		client, client_address = SERVER.accept()
		print("%s:%s has connected." % client_address)
		addresses[client] = client_address
		Thread(target = call, args = (client,)).start()

def launch(browser,pw):
    page = browser.new_page()
    count = 0
    while True:
        page.goto("https://character-ai.us.auth0.com/u/login?state=hKFo2SA2UWpDVjJLanBBRHRtUkl5ZGxKanhyelloRzVCaDd0NaFur3VuaXZlcnNhbC1sb2dpbqN0aWTZIDRaTUtMQkt4UTNKU2tfbnVWbGxyUUZvZURpTW5ld0x0o2NpZNkgZHlEM2dFMjgxTXFnSVNHN0Z1SVhZaEwyV0VrbnFaenY")
        #page.wait_for_load_state()
        #wait for button
        #page.wait_for_selector("button[type=button]")
        count += 1
        if count == 5:
            print("Can't click first button")
            return
        try:
            page.click("button[type=button]",timeout=5000)
            break
        except:
            browser.close()
            pw.stop()
            pw = sync_playwright().start()
            if DEBUG_MODE:
                browser = pw.firefox.launch(headless=False)
            else:
                browser = pw.firefox.launch()
            page = browser.new_page()
        # if page.is_visible("[id=rcc-confirm-button]"):
        #     break
    page.click("[id=rcc-confirm-button]",timeout=5000)
    page.click('[class="btn btn-primary btn-sm"]',timeout=5000)
    page.click('[class=" btn border"]',timeout=5000)
    page.fill("input#username",USERNAME,timeout=5000)
    page.fill("input#password",PASSWORD,timeout=5000)
    page.click("button[type=submit]")
    try:
        page.click('[href="/chats"]')
    except:
        print("Email or password incorrect or captcha not solved")
        return
    # except:
    #     page.fill("input#password",PASSWORD)
    #     time_first = time.time()
    #     while not page.is_visible('[href="/chats"]') and time.time()-time_first < 10:
    #         page.wait_for_timeout(5000)
    #     page.click('[href="/chats"]')
    char_page = characters_pages[CHOOSE_CHARACTER]
    if page.is_visible(char_page):
         page.click(char_page,timeout=500)
    else:
        try:
            page.click('[href="/search?"]',timeout=5000)
            page.fill("input#search-input","monika",timeout=5000)
            page.click('[class="btn btn-primary"]',delay=2000,timeout=5000)
            time_init = time.time()
            while not page.is_visible(char_page) and time.time()-time_init < 30:
                page.mouse.wheel(0,50)
            page.click(char_page,timeout=5000)
        except:
            print("Character not found")
            return
    page.click('[class="col-auto px-2 dropdown"]',timeout=5000)
    page.click('text=Save and Start New Chat')
    return page

def call(client):
    thread = Thread(target=listenToClient, args=(client,), daemon=True)
    thread.start()

#Launch the game
subprocess.Popen(GAME_PATH+'\DDLC.exe')

def post_message(page, message):
    if message == "QUIT":
        page.fill("textarea","I'll be right back")
    else:
        page.fill("textarea",message)
    while True:
        try:
            page.click('[class="btn py-0"]')
            break
        except:
            pass
    
def listenToClient(client):
    """ Get client username """
    name = "User"
    clients[client] = name
    launched = False
    while True:
        received_msg = client.recv(BUFSIZE).decode("utf-8") #Message indicating the mode used (chatbot,camera_int or camera)
        received_msg = received_msg.split("/m")
        rest_msg = received_msg[1]
        received_msg = received_msg[0]
        if received_msg == "chatbot":
            if '/g' in rest_msg:
                received_msg , step = rest_msg.split("/g")
            else:
                received_msg = client.recv(BUFSIZE).decode("utf-8") #Message containing the user input
                received_msg , step = received_msg.split("/g")
            step = int(step)

            #Speech to text
            if received_msg == "begin_record":

                with sr.Microphone(sample_rate=16000) as source:
                    sendMessage("yes".encode("utf-8"))
                    #get and save audio to wav file
                    audio = r.listen(source)
                    torch_audio = torch.from_numpy(np.frombuffer(audio.get_raw_data(), np.int16).flatten().astype(np.float32) / 32768.0)
                    audio_data = torch_audio
                    if english:
                        result = audio_model.transcribe(audio_data,language='english')
                    else:
                        result = audio_model.transcribe(audio_data)
                    received_msg = result['text']

            print("User: "+received_msg)

            if USE_CHARACTER_AI:
                if not launched:
                    try:
                        pw = sync_playwright().start()
                        if DEBUG_MODE:
                            browser =  pw.firefox.launch(headless=False)
                        else:
                            browser =  pw.firefox.launch()
                        page = launch(browser,pw)
                        if page == None:
                            sendMessage("server_error".encode("utf-8"))
                            pw.stop()
                            continue
                        launched = True
                        sendMessage("server_ok".encode("utf-8"))
                    except:
                        sendMessage("server_error".encode("utf-8"))
                        pw.stop()
                        continue
                
                if os.path.exists(GAME_PATH+'/game/Submods/AI_submod/audio/out.ogg'):
                    os.remove(GAME_PATH+'/game/Submods/AI_submod/audio/out.ogg')
                time.sleep(2)
                post_message(page,received_msg)

                while True:
                    if not page.is_disabled('[class="btn py-0"]'):
                        query =  page.query_selector_all(('[class="markdown-wrapper markdown-wrapper-last-msg swiper-no-swiping"]'))
                        if len(query) > 0:
                            msg =  query[0].inner_html()
                        else:
                            post_message(page,received_msg)
                            continue
                        
                        msg = msg.replace("<em>","{i}")
                        msg = msg.replace("</em>","{/i}")
                        msg = msg.replace("<div>","")
                        msg = msg.replace("</div>","")
                        msg = msg.replace("<p>","\n")
                        msg = msg.replace("</p>","")
                        msg = msg.replace("<del>","")
                        msg = msg.replace("</del>","")
                        msg = msg.replace("<br>","")
                        msg = msg.replace("<br/>","")
                        msg = msg.replace('<div style="overflow-wrap: break-word;">',"")
                        msg = msg.replace("&lt;","<")
                        msg = msg.replace("&gt;",">")

                        if received_msg != "QUIT":       

                            #TTS addition
                            if USE_TTS:
                                print("Using TTS")
                                msg_audio = msg.replace("\n"," ")
                                msg_audio = msg_audio.replace("{i}","")
                                msg_audio = msg_audio.replace("{/i}",".")
                                msg_audio = msg_audio.replace("~","!")
                                subprocess.check_call(['tts', '--text', msg_audio, '--model_name', 'tts_models/multilingual/multi-dataset/your_tts', '--speaker_wav', 'audios/talk_13.wav', '--language_idx', 'en', '--out_path', GAME_PATH + '/game/Submods/AI_submod/audio/out.wav'])
                                def playVoice():
                                    f = open(GAME_PATH+'/game/Submods/AI_submod/audio/out.wav', 'rb')
                                    audio = f.read()
                                    f.close()
                                    play_obj = sa.play_buffer(audio, 1, 2, 16000)
                                    play_obj.wait_done()
                                    
                                    os.remove(GAME_PATH+'/game/Submods/AI_submod/audio/out.wav')
                                thread_voice = Thread(target=playVoice, args=(), daemon=True)
                                thread_voice.start()    
                       
                            emotion = "".encode("utf-8")
                            msg = msg.encode("utf-8")   
                            msg_to_send = msg + b"/g" + emotion
                            print("Sent: "+ msg_to_send.decode("utf-8"))
                            sendMessage(msg_to_send)
                        break
                    
        else:
            counter = received_msg[6:]
            counter = int(counter)
            msg = "no_data"
            msg = msg.encode()
            sendMessage(msg)


def sendMessage(msg, name=""):
    """ send message to all users present in 
    the chat room"""
    for client in clients:
        client.send(bytes(name, "utf8") + msg)

if __name__ == "__main__":
    SERVER.listen(5)
    ACCEPT_THREAD = Thread(target=listen)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()