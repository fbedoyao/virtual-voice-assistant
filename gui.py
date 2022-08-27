import speech_recognition as sr
import pyttsx3
import pywhatkit
import wikipedia
import os
import subprocess as sub
from tkinter import *
from PIL import Image, ImageTk
import threading as tr
import pymysql



main_window = Tk()
main_window.title("Sophia")

main_window.geometry("800x450")
main_window.resizable(0, 0)
main_window.configure(bg="#302b63")


commands = """
            Available commands:

            - Play ... (song)
            - Search for ... (something)
            - Open ... (website or .exe)
            - File ... (file name)
            - Terminate
"""

label_title = Label(main_window, text = "Sophia", bg = "#200122", fg = "#c0c0aa", font = ("Arial", 30, "bold"))
label_title.pack(pady=10)

canvas_commands = Canvas(bg="#200122", height = 170, width = 220)
canvas_commands.place(x=0, y=0)
canvas_commands.create_text(90, 80, text=commands, fill="white", font = 'Arial 10')

text_info = Text(main_window, bg = "white", fg= "#200122")
text_info.place(x=0, y=175, height = 280, width = 225)

sophia_photo = (Image.open("sophia-img.png"))
resized_image= sophia_photo.resize((225,225), Image.Resampling.LANCZOS)
new_image= ImageTk.PhotoImage(resized_image)
window_photo = Label(main_window, image= new_image, bg="#302b63")
window_photo.pack(pady = 5)

name = "sophia"

listener = sr.Recognizer()

engine = pyttsx3.init()

voices = engine.getProperty('voices')

engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 170)



def talk(text):
    engine.say(text)
    engine.runAndWait()

def read_and_talk():
    text = text_info.get("1.0", "end")
    talk(text)

def write_text(text):
    text_info.insert(INSERT, text)

def listen():
    try:
        with sr.Microphone() as source:
            talk("I'm listening ...")
            pc = listener.listen(source)
            rec = listener.recognize_google(pc)
            rec = rec.lower()
            if name in rec:
                rec = rec.replace(name, '')
            print(rec)
    except:
        pass

    return rec

try:
    conn = pymysql.connect(host="localhost", user = "root", password = "", db="mysql")
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS sophia_brain")
    talk("Succesful connection to the database!")
    conn.commit()
    conn.close()
    cursor.close()


except:
    talk("Error connecting to the database.")
    exit()

try:
    conn = pymysql.connect(host = "localhost", user = "root", password="", db="sophia_brain")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS files (file_name varchar(255), file_path varchar(255), PRIMARY KEY (file_name))")
    cursor.execute("CREATE TABLE IF NOT EXISTS programs (program_name varchar(255), program_path varchar(255), PRIMARY KEY (program_name))")
    cursor.execute("CREATE TABLE IF NOT EXISTS sites (site_name varchar(255), site_url varchar(255), PRIMARY KEY (site_name))")

    conn.commit()
    conn.close()
    cursor.close()
    talk("Succesfully initialized all systems!")

except:
    talk("Error initializing all systems.")
    exit()

def write(f):
    talk("Sure! What do you want me to write?")
    rec_write = listen()
    f.write(rec_write + os.linesep)
    f.close()
    talk("Done!")
    sub.Popen("note.txt", shell=True)



def run_sophia():

        rec = listen()
        if 'play' in rec:
            music = rec.replace('play', '')
            print("Playing " + music)
            talk("Playing " + music)
            pywhatkit.playonyt(music)

        elif 'search for' in rec:
            try:
                search = rec.replace('search for', '')
                wiki = wikipedia.summary(search, 1)
                talk(wiki)
                write_text(search + " : " + wiki)
            except:
                talk("Sorry, I couldn't find anything.")
                pass

        elif 'open' in rec:
            task = rec.replace('open', '').strip()
            #if task in sites:
            #    for task in sites:
            #        if task in rec:
            #            sub.call(f'start chrome.exe {sites[task]}', shell=True)
            #            talk(f'Opening {task}')
            #elif task in programs:
            #    for task in programs:
            #        if task in rec:
            #            talk(f"Opening {task}")
            #            os.startfile(programs[task])
            #else:
            #    talk("I'm sorry, you haven't saved that website or program yet.")
            try:
                conn = pymysql.connect(host = "localhost", user = "root", password="", db="sophia_brain")
                cursor = conn.cursor()
                cursor2 = conn.cursor()
                web_num = cursor.execute(f'SELECT site_url FROM sites WHERE site_name = "{task}"')
                programs_num = cursor2.execute(f'SELECT program_path FROM programs WHERE program_name = "{task}"')
                conn.commit()
                if web_num != 0:
                    result = cursor.fetchone()[0]
                    formatted_result = (result[1:len(result)-1])
                    sub.call(f'start chrome.exe {formatted_result}', shell=True)
                    talk(f'Opening {task}')

                elif programs_num != 0:
                    result = cursor2.fetchone()[0]
                    formatted_result = (result[1:len(result)-1])
                    os.startfile(formatted_result)
                    talk(f'Opening {task}')
                else:
                    talk(f'You haven\'t saved {task} in your programs or websites yet.')
            except:
                talk("Error")


        elif 'file' in rec:
            file = rec.replace('file', '').strip()
            #if file in files:
            #    for file in files:
            #        if file in rec:
            #            sub.Popen(files[file], shell=True)
            #            talk(f'Opening {file}')
            #else:
            #    talk("I'm sorry, you haven't saved that file yet.")
            try:
                conn = pymysql.connect(host = "localhost", user = "root", password="", db="sophia_brain")
                cursor = conn.cursor()
                result_num = cursor.execute(f'SELECT file_path FROM files WHERE file_name = "{file}"')
                conn.commit()
                if result_num == 0:
                    talk(f'You haven\'t saved {file} in your files yet.')
                else :
                    result = cursor.fetchone()[0]
                    formatted_result = (result[1:len(result)-1])
                    sub.Popen(formatted_result, shell=True)
                    talk(f'Opening {file}')
                conn.close()
                cursor.close()

            except:
                talk("Error")
                pass


        elif 'write' in rec:
            try:
                with open("note.txt", 'w') as f:
                    write(f)
            except FileNotFoundError as e:
                file = open("note.txt", 'w')
                write(file)
        elif 'terminate' in rec:
            exit()

def open_file():

    global entry_file_name, entry_file_path
    window = Toplevel()
    window.title("Add a file")
    window.configure(bg="gray")
    window.geometry("300x200")
    window.resizable(0, 0)
    main_window.eval(f'tk::PlaceWindow {str(window)} center')

    label_title = Label(window, text = "Add file", bg = "gray", fg = "black", font = ("Arial", 15, "bold"))
    label_title.pack(pady = 3)

    label_name = Label(window, text = "File Name", bg = "gray", fg = "black", font = ("Arial", 10))
    label_name.pack(pady = 2)

    entry_file_name = Entry(window)
    entry_file_name.pack(pady=2)


    label_path = Label(window, text = "File Path", bg = "gray", fg = "black", font = ("Arial", 10))
    label_path.pack(pady = 2)

    entry_file_path = Entry(window, width=40)
    entry_file_path.pack(pady=2)

    button_save = Button(window, text="Save", fg="white", bg="black", font = ("Arial", 10, "bold"), command = add_file)
    button_save.pack(pady = 3)

def open_program():

    global entry_program_name, entry_program_path

    window = Toplevel()
    window.title("Add Program")
    window.configure(bg="gray")
    window.geometry("300x200")
    window.resizable(0, 0)
    main_window.eval(f'tk::PlaceWindow {str(window)} center')

    label_title = Label(window, text = "Add Program", bg = "gray", fg = "black", font = ("Arial", 15, "bold"))
    label_title.pack(pady = 3)

    label_name = Label(window, text = "Program Name", bg = "gray", fg = "black", font = ("Arial", 10))
    label_name.pack(pady = 2)

    entry_program_name = Entry(window)
    entry_program_name.pack(pady=2)


    label_path = Label(window, text = "Program Path", bg = "gray", fg = "black", font = ("Arial", 10))
    label_path.pack(pady = 2)

    entry_program_path = Entry(window, width = 40)
    entry_program_path.pack(pady=2)

    button_save = Button(window, text="Save", fg="white", bg="black", font = ("Arial", 10, "bold"), command = add_program)
    button_save.pack(pady = 3)

def open_website():

    global entry_website_name, entry_website_url

    window = Toplevel()
    window.title("Add Website")
    window.configure(bg="gray")
    window.geometry("300x200")
    window.resizable(0, 0)
    main_window.eval(f'tk::PlaceWindow {str(window)} center')

    label_title = Label(window, text = "Add Website", bg = "gray", fg = "black", font = ("Arial", 15, "bold"))
    label_title.pack(pady = 3)

    label_name = Label(window, text = "Website Name", bg = "gray", fg = "black", font = ("Arial", 10))
    label_name.pack(pady = 2)

    entry_website_name = Entry(window)
    entry_website_name.pack(pady=2)


    label_path = Label(window, text = "URL", bg = "gray", fg = "black", font = ("Arial", 10))
    label_path.pack(pady = 2)

    entry_website_url = Entry(window, width = 40)
    entry_website_url.pack(pady=2)

    button_save = Button(window, text="Save", fg="white", bg="black", font = ("Arial", 10, "bold"), command = add_website)
    button_save.pack(pady = 3)



def add_file():
    file_name = entry_file_name.get().strip()
    file_path = entry_file_path.get().strip()

    #files[file_name] = file_path
    try:
        conn = pymysql.connect(host = "localhost", user = "root", password="", db="sophia_brain")
        cursor = conn.cursor()
        query = f'INSERT INTO files VALUES ("{file_name}","{repr(file_path)}")'
        cursor.execute(query)
        conn.commit()
        conn.close()
        cursor.close()
        talk(f'Added {file_name} to your files')
        entry_file_name.delete(0, "end")
        entry_file_path.delete(0, "end")

    except:
        talk(f'Error inserting {file_name} into your files')
    

def add_program():
    program_name = entry_program_name.get().strip()
    program_path = entry_program_path.get().strip()

    #programs[program_name] = program_path
    try:
        conn = pymysql.connect(host = "localhost", user = "root", password="", db="sophia_brain")
        cursor = conn.cursor()
        query = f'INSERT INTO programs VALUES ("{program_name}","{repr(program_path)}")'
        cursor.execute(query)
        conn.commit()
        conn.close()
        cursor.close()
        talk(f'Added {program_name} to your programs')
        entry_program_name.delete(0, "end")
        entry_program_path.delete(0, "end")

    except:
        talk(f'Error inserting {program_name} into your programs')

def add_website():
    website_name = entry_website_name.get().strip()
    website_url = entry_website_url.get().strip()

    #sites[website_name] = website_url
    try:
        conn = pymysql.connect(host = "localhost", user = "root", password="", db="sophia_brain")
        cursor = conn.cursor()
        query = f'INSERT INTO sites VALUES ("{website_name}","{repr(website_url)}")'
        cursor.execute(query)
        conn.commit()
        conn.close()
        cursor.close()
        talk(f'Added {website_name} to your web sites')
        entry_website_name.delete(0, "end")
        entry_website_url.delete(0, "end")

    except:
        talk(f'Error inserting {website_name} into your web sites')




button_listen = Button(main_window, text="Talk", fg="white", bg="#200122", font = ("Arial", 15, "bold"), command = run_sophia)
button_listen.pack(pady = 10)

button_speak = Button(main_window, text="Read", fg="white", bg="#200122", font = ("Arial", 10, "bold"), command = read_and_talk)
button_speak.place(x=625, y = 80, width=100, height=30)

button_add_files = Button(main_window, text="Add Files", fg="white", bg="#200122", font = ("Arial", 10, "bold"), command = open_file)
button_add_files.place(x=625, y = 120, width=100, height=30)

button_add_programs = Button(main_window, text="Add Programs", fg="white", bg="#200122", font = ("Arial", 10, "bold"), command = open_program)
button_add_programs.place(x=625, y = 160, width=100, height=30)

button_add_sites = Button(main_window, text="Add Websites", fg="white", bg="#200122", font = ("Arial", 10, "bold"), command = open_website)
button_add_sites.place(x=625, y = 200, width=100, height=30)

main_window.mainloop() 

