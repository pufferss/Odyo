from pytube import YouTube
import os
import platform
import subprocess
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import asksaveasfilename
import base64


def convert():
    try:
        done.grid_forget()
        youtube = YouTube(url.get())
        errorMSG.grid_forget()

        # 140 correspond au .mp4 audio seulement en 128kb/s
        video = youtube.streams.get_by_itag(140)
        global file_name
        global file_path
        if not file_name:
            file_name = youtube.title
            for k in forbidden_chars:
                file_name = file_name.replace(k, '')
            file_name += '.mp3'
        video.download(output_path=file_path, filename=file_name)
        done.grid(column=1)
        file_name = ''
    except:
        errorMSG.grid(column=0, columnspan=2)


def savePath():
    global file_name
    global file_path
    path = asksaveasfilename(
        defaultextension='.mp3', initialdir=file_path, filetypes=[("mp3 files", ".mp3")])
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

window = Tk()
window.geometry('500x300')
window.resizable(False, False)
window.title('ODYO Downloader')
icon ='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'
icon = PhotoImage(data=base64.b64decode(icon))
window.wm_iconphoto(True, icon)
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)
frm = ttk.Frame(window)
frm.grid()

url = StringVar()
file_path = str()
file_name = str()
operating_sys = platform.system()
user = os.getlogin()
forbidden_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']

checkOS()

text = ttk.Label(frm, text='Lien de la vidéo:')
text.grid(column=1)
text.grid_rowconfigure(1, weight=1)
text.grid_columnconfigure(1, weight=1)


url_textbox = ttk.Entry(frm, width=50, textvariable=url)
url_textbox.focus()
url_textbox.grid(column=1, pady=20)
url_textbox.grid_rowconfigure(1, weight=1)
url_textbox.grid_columnconfigure(1, weight=1)


browse = ttk.Button(frm, text='Parcourir', command=savePath, cursor='hand2')
browse.grid(column=1)
browse.grid_rowconfigure(1, weight=1)
browse.grid_columnconfigure(1, weight=1)

label_path = ttk.Label(
    frm, text='Le fichier sera téléchargé vers: ' + file_path)
label_path.grid(column=1)
label_path.grid_rowconfigure(1, weight=1)
label_path.grid_columnconfigure(1, weight=1)

convertir = ttk.Button(frm, text='Convertir', command=convert, cursor='hand2')
convertir.grid(column=1, pady=10)
convertir.grid_rowconfigure(1, weight=1)
convertir.grid_columnconfigure(1, weight=1)

done = ttk.Label(frm, text='Télechargement Terminé !', foreground='green')
done.grid_rowconfigure(1, weight=1)
done.grid_columnconfigure(1, weight=1)

errorMSG = ttk.Label(frm, text='Erreur: Lien invalide !', foreground='red')
errorMSG.grid_rowconfigure(1, weight=1)
errorMSG.grid_columnconfigure(1, weight=1)

window.mainloop()
