from pytube import YouTube
import os
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import asksaveasfilename

def convert():
    try:
        youtube = YouTube(url.get())
        errorMSG.grid_forget()
        
        video = youtube.streams.get_by_itag(140)# 140 correspond au .mp4 audio suelement en 128kb/s
        #outfile = video.download(output_path='/home/puff/Musique/', filename=file_name)
        global file_name
        global file_path
        if not file_name:
            file_name = youtube.title + '.mp3'
        if not file_path:
            file_path = '/home/puff/Musique'
        video.download(output_path=file_path, filename=file_name)
        # rename fichier de sortie
        #base, ext = os.path.splitext(outfile)
        #newfile = base + '.mp3'
        #print(newfile)
        #os.rename(outfile, newfile)
    except:
        errorMSG.grid(column=0, row=4, columnspan=2)

def savePath():
    path = asksaveasfilename(defaultextension='.mp3')
    if not path:
        return
    global file_name
    global file_path
    file_path, file_name = os.path.split(path)


window = Tk()
window.geometry("500x300")
window.resizable(False,False)
window.title("Youtube Downloader")
frm = ttk.Frame(window)
frm.grid()
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

url = StringVar()
file_path = str()
file_name = str()

text = ttk.Label(frm, text="Lien de la vidéo:")
text.grid(column=1)
text.grid_rowconfigure(1, weight=1)
text.grid_columnconfigure(1, weight=1)


url_textbox = ttk.Entry(frm, width=50, textvariable=url)
url_textbox.focus()
url_textbox.grid(column=1, row=1, pady=20)
url_textbox.grid_rowconfigure(1, weight=1)
url_textbox.grid_columnconfigure(1, weight=1)

browse = ttk.Button(frm, text='Parcourir', command=savePath)
browse.grid(column=1, row=2)
browse.grid_rowconfigure(1, weight=1)
browse.grid_columnconfigure(1, weight=1)

convertir = ttk.Button(frm, text="Convertir", command=convert)
convertir.grid(column=1,row=3)
convertir.grid_rowconfigure(1, weight=1)
convertir.grid_columnconfigure(1, weight=1)

errorMSG = ttk.Label(frm, text='Veuillez écrire le lien d\'une vidéo')
errorMSG.grid_rowconfigure(1, weight=1)
errorMSG.grid_columnconfigure(1, weight=1)

window.mainloop()