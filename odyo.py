from pytube import YouTube
import os
import platform
import subprocess
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import asksaveasfilename
import base64
import re
import ffmpeg
from threading import Thread

def func_thread():
    th=Thread(target= lambda: convert(), daemon=True)
    th.start()

def convert():
    try:
        done.grid_forget()
        errorMSG.grid_forget()
        global file_name
        global file_path
        if file_name.split('.')[-1] != extension.get().split('.')[-1] and file_name != '':
            file_name = file_name.split('.')[0] + extension.get()
        if re.search(".*yout.*", url.get()):
            
            youtube = YouTube(url.get())
           
            if not file_name:
                file_name = youtube.title
                for k in forbidden_chars:
                    file_name = file_name.replace(k, '')
                file_name += extension.get()

            if extension.get() == '.mp4':
                video = youtube.streams.filter(adaptive=True, file_extension='mp4').first()
                if video.resolution != '1080p':
                    video = youtube.streams.filter(progressive=True,file_extension='mp4').get_highest_resolution()
                    video.download(output_path=file_path, filename=file_name)
                else:
                    video.download(output_path=file_path, filename='TEMP' + file_name)
                    audio = youtube.streams.filter(only_audio=True, file_extension='mp4', adaptive=True).order_by('codecs').first()
                    audio.download(output_path=file_path, filename='TEMP' + file_name.split('.')[0] + '.mp3')
                    combine_files()

            elif extension.get() == '.mp3':
                video = youtube.streams.filter(only_audio=True, file_extension='mp4', adaptive=True).order_by('codecs').first()

            
                video.download(output_path=file_path, filename=file_name)

        else:
            raise errorMSG.grid(column=1, columnspan=2)
        
        done.grid(column=1, columnspan=3)
    except:
        print('ERREUR TOTAL')
        errorMSG.grid(column=1, columnspan=3)
        try:
            os.remove(file_path + '/' + 'TEMP' +file_name)
            os.remove(file_path + '/' + file_name.split('.')[0] + '.mp3')
        except:
            return
    
    file_name = ''

def combine_files():
    global file_name
    global file_path
    input_vid = ffmpeg.input(file_path + '/' + 'TEMP' + file_name)
    input_aud = ffmpeg.input(file_path + '/' + 'TEMP' + file_name.split('.')[0] + '.mp3')
    ffmpeg.concat(input_vid, input_aud, v=1, a=1, unsafe= True)
    
    ffmpeg.output(input_vid.video, input_aud.audio, file_path + '/' + file_name, codec='copy').overwrite_output().run(quiet=True)

    os.remove(file_path + '/' + 'TEMP' + file_name)
    os.remove(file_path + '/' + 'TEMP' + file_name.split('.')[0] + '.mp3')


def savePath():
    global file_name
    global file_path
    path = asksaveasfilename(
        defaultextension=extension.get(), initialdir=file_path, filetypes=[('MP3 & MP4', '*.mp3' '*.mp4')])
    if not path:
        return
    file_path, file_name = os.path.split(path)
    label_path.config(text='Le fichier sera téléchargé vers: ' + file_path)


def checkOS():
    global file_path
    if operating_sys == 'Linux':
        file_path = str(subprocess.check_output(
            ['xdg-user-dir', 'DESKTOP']).decode('ascii')).rstrip()
    elif operating_sys == 'Windows':
        file_path = 'C:/Users/' + user + '/Desktop'
    elif operating_sys == 'Darwin':
        file_path = '~/Desktop'


window = Tk(className='Odyo Downloader')
window.geometry('500x300')
window.resizable(False, False)
window.title('ODYO Downloader')
icon = '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'
icon = PhotoImage(data=base64.b64decode(icon))
window.wm_iconphoto(True, icon)
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)
frm = ttk.Frame(window)
frm.grid()

url = StringVar()
file_path = str()
file_name = str()
progress = IntVar()
operating_sys = platform.system()
user = os.getlogin()
forbidden_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']

checkOS()

text = ttk.Label(frm, text='Lien de la vidéo:')
text.grid(column=1, columnspan=3)
text.grid_rowconfigure(1, weight=1)
text.grid_columnconfigure(1, weight=1)


url_textbox = ttk.Entry(frm, width=45, textvariable=url)
url_textbox.focus()
url_textbox.grid(column=1, pady=20, columnspan=2)
url_textbox.grid_rowconfigure(1, weight=1)
url_textbox.grid_columnconfigure(1, weight=1)

ext = StringVar()
L_Extension = ['.mp3', '.mp4']
extension = ttk.Combobox(frm, values=L_Extension,
                         state="readonly", width='5', textvariable=ext)
extension.current(1)
extension.grid(column=3, row=1)
extension.grid_rowconfigure(1, weight=1)
extension.grid_columnconfigure(1, weight=1)


browse = ttk.Button(frm, text='Parcourir', command=savePath, cursor='hand2')
browse.grid(column=1, columnspan=3)
browse.grid_rowconfigure(1, weight=1)
browse.grid_columnconfigure(1, weight=1)

label_path = ttk.Label(
    frm, text='Le fichier sera téléchargé vers: ' + file_path)
label_path.grid(column=1, columnspan=3, pady=7)
label_path.grid_rowconfigure(1, weight=1)
label_path.grid_columnconfigure(1, weight=1)

convertir = ttk.Button(frm, text='Convertir', command=func_thread, cursor='hand2')
convertir.grid(column=1, columnspan=3)
convertir.grid_rowconfigure(1, weight=1)
convertir.grid_columnconfigure(1, weight=1)

done = ttk.Label(frm, text='Télechargement Terminé !', foreground='green')
done.grid_rowconfigure(1, weight=1)
done.grid_columnconfigure(1, weight=1)

errorMSG = ttk.Label(frm, text='Erreur: Lien invalide !', foreground='red')
errorMSG.grid_rowconfigure(1, weight=1)
errorMSG.grid_columnconfigure(1, weight=1)

window.mainloop()
