from pytube import YouTube
import os
from tkinter import *
from tkinter import ttk


def convert():
    try:
        youtube = YouTube(url.get())
        # 140 correspond au .mp4 audio suelement en 128kb/s
        video = youtube.streams.get_by_itag(140)
        outfile = video.download('/home/puff/Musique')

        errorMSG.grid_forget()
        # rename fichier de sortie
        base, ext = os.path.splitext(outfile)
        newfile = base + '.mp3'
        os.rename(outfile, newfile)
    except:
        errorMSG.grid(column=0, row=2, columnspan=2)


window = Tk()
window.geometry("700x400")
frm = ttk.Frame(window)
frm.grid()
ttk.Label(frm, text="Lien de la vidéo:").grid()
url = StringVar()

url_textbox = ttk.Entry(frm, width=50, textvariable=url)
url_textbox.focus()
url_textbox.grid(column=1, row=0)

convertir = ttk.Button(frm, text="Convertir", command=convert).grid(row=1)
errorMSG = ttk.Label(frm, text='Veuillez écrire le lien d\'une vidéo')

window.mainloop()
