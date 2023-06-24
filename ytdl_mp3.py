from pytube import YouTube
import os
from tkinter import *
from tkinter import ttk


def convert():
    try:
        youtube = YouTube(url.get())
        errorMSG.grid_forget()
        # 140 correspond au .mp4 audio suelement en 128kb/s
        video = youtube.streams.get_by_itag(140)
        outfile = video.download('/home/puff/Musique')

        # rename fichier de sortie
        base, ext = os.path.splitext(outfile)
        newfile = base + '.mp3'
        os.rename(outfile, newfile)
    except:
        errorMSG.grid(column=0, row=3, columnspan=2)


window = Tk()
window.geometry("500x150")
window.resizable(False,False)
window.title("Youtube Downloader")
frm = ttk.Frame(window)
frm.grid()
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

text = ttk.Label(frm, text="Lien de la vidéo:")
text.grid(column=1)
text.grid_rowconfigure(1, weight=1)
text.grid_columnconfigure(1, weight=1)

url = StringVar()

url_textbox = ttk.Entry(frm, width=50, textvariable=url)
url_textbox.focus()
url_textbox.grid(column=1, row=1, pady=20)
url_textbox.grid_rowconfigure(1, weight=1)
url_textbox.grid_columnconfigure(1, weight=1)

convertir = ttk.Button(frm, text="Convertir", command=convert)
convertir.grid(column=1,row=2)
convertir.grid_rowconfigure(1, weight=1)
convertir.grid_columnconfigure(1, weight=1)

errorMSG = ttk.Label(frm, text='Veuillez écrire le lien d\'une vidéo')
errorMSG.grid_rowconfigure(1, weight=1)
errorMSG.grid_columnconfigure(1, weight=1)

window.mainloop()
