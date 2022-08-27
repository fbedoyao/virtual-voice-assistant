import speech_recognition as sr
import pyttsx3, pywhatkit, wikipedia, datetime, keyboard, os
from pygame import mixer
import subprocess as sub

name = "sophia"

listener = sr.Recognizer()

engine = pyttsx3.init()

voices = engine.getProperty('voices')

engine .setProperty('voice', voices[1].id)

sites = {
    'google': 'google.com',
    'youtube': 'youtube.com',
    'facebook': 'facebook.com',
    'whatsapp': 'web.whatsapp.com'
}

files = {
    'important': 'important.txt'
}

telegram_path = r'asbhja\ndfasfwe'

programs = {
    'telegram': r'C:\Users\user\AppData\Roaming\Telegram Desktop\Telegram.exe'
}



def talk(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    try:
        with sr.Microphone() as source:
            print("Listening ...")
            pc = listener.listen(source)
            rec = listener.recognize_google(pc)
            rec = rec.lower()
            if name in rec:
                rec = rec.replace(name, '')
    except:
        pass

    return rec

def write(f):
    talk("Sure! What do you want me to write?")
    rec_write = listen()
    f.write(rec_write + os.linesep)
    f.close()
    talk("Done!")
    sub.Popen("note.txt", shell=True)

def run_sophia():

    while True:
        rec = listen()
        if 'play' in rec:
            music = rec.replace('play', '')
            print("Playing " + music)
            talk("Playing " + music)
            pywhatkit.playonyt(music)

        elif 'search for' in rec:
            try :
                search = rec.replace('search for', '')
                wiki = wikipedia.summary(search, 1)
                print("Searching: " + wiki)
                talk(wiki)
            except:
                talk("Sorry, I couldn't find anything.")
                break
        
        elif 'open' in rec:
            for site in sites :
                if site in rec:
                    sub.call(f'start chrome.exe {sites[site]}', shell = True )
                    talk(f'Opening {site}')
            for app in programs :
                if app in rec:
                    talk(f"Opening {app}")
                    os.startfile(programs[app])

        elif 'file' in rec:
            for file in files:
                if file in rec:
                    sub.Popen(files[file], shell = True)
                    talk(f'Opening {file}')

        elif 'write' in rec:
            try:
                with open("note.txt", 'w') as f:
                    write(f)
            except FileNotFoundError as e:
                file = open("note.txt", 'w')
                write(file)
        elif 'terminate' in rec:
            break


        


if __name__ == '__main__':
    run_sophia()

