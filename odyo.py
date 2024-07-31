from pytubefix import YouTube
from pytubefix import Playlist
from pytubefix.exceptions import AgeRestrictedError
from pytubefix.exceptions import VideoPrivate
from pytubefix.exceptions import VideoRegionBlocked

import os
import platform
import subprocess
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askdirectory
import base64
import re
import ffmpeg
from threading import Thread

def func_thread():
    th=Thread(target= lambda: convert(), daemon=True)
    th.start()

def odyo_download(youtube):
    in_progress.grid(column=1, columnspan=4)
    if extension.get() == '.mp4':
        
        if quality.get() == 'Max':
            video = youtube.streams.filter(subtype='mp4', adaptive=True).first()
        else:
            video = youtube.streams.filter(res=quality.get().split(' ')[0], subtype='mp4', adaptive=True).first()
            if video == None:
                in_progress.grid_forget()
                errorMSG.configure(text='Erreur: Qualité sélectionée non disponible !')
                errorMSG.grid(column=1, columnspan=4)
                return False
            
        print(video)


        video.download(output_path=file_path, filename= 'TEMP' + file_name)
        audio = youtube.streams.filter(only_audio=True, file_extension='mp4', adaptive=True).order_by('codecs').first()
        audio.download(output_path=file_path, filename= 'TEMP' + file_name.split('.')[0] + '.mp3')
        combine_files()
        return True

    else:
        video = youtube.streams.filter(only_audio=True, file_extension='mp4', adaptive=True).order_by('codecs').first()
        video.download(output_path=file_path, filename='TEMP' + file_name)
        input_aud = ffmpeg.input(file_path + '/' + 'TEMP' + file_name)
        ffmpeg.output(input_aud.audio, file_path + '/' + file_name.split('.')[0] + '.mp3').overwrite_output().run(quiet=True)
        os.remove(file_path + '/' + 'TEMP' + file_name)
        return True


def convert():
    try:
        done.grid_forget()
        errorMSG.grid_forget()
        in_progress.grid_forget()
        global file_name
        global file_path

        if re.search(".*yout.*", url.get()):
            if re.search(".*playlist.*", url.get()):
                p = Playlist(url.get())
                for playlist_video in p.videos:
                    file_name = playlist_video.title
                    for k in forbidden_chars:
                        file_name = file_name.replace(k, '')
                    file_name += '.mp4'

                    if not odyo_download(playlist_video):
                        return

            else:
                youtube = YouTube(url.get())
            
                file_name = youtube.title
                for k in forbidden_chars:
                    file_name = file_name.replace(k, '')
                file_name += '.mp4'
                

                if not odyo_download(youtube):
                    return



        else:
            errorMSG.configure(text='Erreur: Lien invalide !')
            errorMSG.grid(column=1, columnspan=4)
            return
        
        in_progress.grid_forget()
        done.grid(column=1, columnspan=4)
    
    except AgeRestrictedError:
        in_progress.grid_forget()
        errorMSG.configure(text='Erreur: Restriction d\'age !')
        errorMSG.grid(column=1, columnspan=4)
    except VideoPrivate:
        in_progress.grid_forget()
        errorMSG.configure(text='Erreur: Vidéo privée !')
        errorMSG.grid(column=1, columnspan=4)
    except VideoRegionBlocked:
        in_progress.grid_forget()
        errorMSG.configure(text='Erreur: Vidéo bloquée dans votre région !')
        errorMSG.grid(column=1, columnspan=4)
    except:
        in_progress.grid_forget()
        errorMSG.configure(text='Erreur: Un problème est survenu !')
        errorMSG.grid(column=1, columnspan=4)
        try:
            os.remove(file_path + '/' + 'TEMP' + file_name)
            os.remove(file_path + '/' + file_name.split('.')[0] + '.mp3')
        except:
            return
    
    

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
    global file_path
    path = askdirectory(initialdir=file_path, mustexist=True)
    if not path:
        return
    file_path = path
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
icon = 'iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAA3NpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDYuMC1jMDA1IDc5LjE2NDU5MCwgMjAyMC8xMi8wOS0xMTo1Nzo0NCAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wTU09Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9tbS8iIHhtbG5zOnN0UmVmPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvc1R5cGUvUmVzb3VyY2VSZWYjIiB4bWxuczp4bXA9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8iIHhtcE1NOk9yaWdpbmFsRG9jdW1lbnRJRD0ieG1wLmRpZDoxOTEwZTQzNS05OTI0LTc4NDEtODFhMi1lYjYzZTAxZjkyZGIiIHhtcE1NOkRvY3VtZW50SUQ9InhtcC5kaWQ6NzFGN0VBRDVCNThGMTFFRUEyMTNFREExNTQzNDEwRUMiIHhtcE1NOkluc3RhbmNlSUQ9InhtcC5paWQ6NzFGN0VBRDRCNThGMTFFRUEyMTNFREExNTQzNDEwRUMiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIDIyLjEgKFdpbmRvd3MpIj4gPHhtcE1NOkRlcml2ZWRGcm9tIHN0UmVmOmluc3RhbmNlSUQ9InhtcC5paWQ6MTkxMGU0MzUtOTkyNC03ODQxLTgxYTItZWI2M2UwMWY5MmRiIiBzdFJlZjpkb2N1bWVudElEPSJ4bXAuZGlkOjE5MTBlNDM1LTk5MjQtNzg0MS04MWEyLWViNjNlMDFmOTJkYiIvPiA8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'
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
forbidden_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*', '.']

checkOS()

text = ttk.Label(frm, text='Lien de la vidéo:')
text.grid(column=1, columnspan=4)
text.grid_rowconfigure(1, weight=1)
text.grid_columnconfigure(1, weight=1)


url_textbox = ttk.Entry(frm, width=40, textvariable=url)
url_textbox.focus()
url_textbox.grid(column=1, pady=20, columnspan=2)
url_textbox.grid_rowconfigure(1, weight=1)
url_textbox.grid_columnconfigure(1, weight=1)

ext = StringVar()
L_Extension = ['.mp3', '.mp4']
extension = ttk.Combobox(frm, values=L_Extension,
                         state="readonly", width='5', textvariable=ext)
extension.current(1)
extension.grid(column=4, row=1)
extension.grid_rowconfigure(1, weight=1)
extension.grid_columnconfigure(1, weight=1)


qual = StringVar()
L_Quality = ['Max', '4320p (8k)', '2160p (4k)', '1440p (2k)', '1080p', '720p', '480p', '360p', '240p', '144p']
quality = ttk.Combobox(frm, values=L_Quality,
                         state="readonly", width='9', textvariable=qual)

quality.current(0)
quality.grid(column=3, row=1)
quality.grid_rowconfigure(1, weight=1)
quality.grid_columnconfigure(1, weight=1)

browse = ttk.Button(frm, text='Parcourir', command=savePath, cursor='hand2')
browse.grid(column=1, columnspan=4)
browse.grid_rowconfigure(1, weight=1)
browse.grid_columnconfigure(1, weight=1)

label_path = ttk.Label(
    frm, text='Le fichier sera téléchargé vers: ' + file_path)
label_path.grid(column=1, columnspan=4, pady=7)
label_path.grid_rowconfigure(1, weight=1)
label_path.grid_columnconfigure(1, weight=1)

convertir = ttk.Button(frm, text='Convertir', command=func_thread, cursor='hand2')
convertir.grid(column=1, columnspan=4)
convertir.grid_rowconfigure(1, weight=1)
convertir.grid_columnconfigure(1, weight=1)

done = ttk.Label(frm, text='Télechargement Terminé !', foreground='green')
done.grid_rowconfigure(1, weight=1)
done.grid_columnconfigure(1, weight=1)

in_progress = ttk.Label(frm, text='En cours de Téléchargement...', foreground='grey')
in_progress.grid_rowconfigure(1, weight=1)
in_progress.grid_columnconfigure(1, weight=1)

errorMSG = ttk.Label(frm, foreground='red')
errorMSG.grid_rowconfigure(1, weight=1)
errorMSG.grid_columnconfigure(1, weight=1)

window.mainloop()