from pytube import YouTube
import os
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import asksaveasfilename

def convert():
    try:
        youtube = YouTube(url.get())
        errorMSG.grid_forget()
        
        video = youtube.streams.get_by_itag(140)# 140 correspond au .mp4 audio seulement en 128kb/s
        global file_name
        global file_path
        if not file_name:
            file_name = youtube.title + '.mp3'
        if not file_path:
            file_path = '/home/puff/Musique'
        video.download(output_path=file_path, filename=file_name)
        done.grid(column=1)
    except:
        errorMSG.grid(column=0, columnspan=2)

def savePath():
    path = asksaveasfilename(defaultextension='.mp3')
    if not path:
        return
    global file_name
    global file_path
    file_path, file_name = os.path.split(path)

window = Tk()
window.geometry('500x300')
window.resizable(False,False)
window.title('Youtube Downloader')
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)
frm = ttk.Frame(window)
frm.grid()

url = StringVar()
file_path = str()
file_name = str()

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