from pytubefix import YouTube
from pytubefix import Playlist
from pytubefix.exceptions import AgeRestrictedError
from pytubefix.exceptions import VideoPrivate
from pytubefix.exceptions import VideoRegionBlocked
import os
import platform
import subprocess
from tkinter.filedialog import askdirectory
import customtkinter as ctk
import base64
import re
import ffmpeg
from threading import Thread
from datetime import datetime

def func_thread():
    th=Thread(target= lambda: convert(), daemon=True)
    th.start()

def odyo_download(youtube):
    app.in_progress.grid(column=1, columnspan=4)
    if app.extension.get() == '.mp4':
        
        if app.quality.get() == 'Max':
            video = youtube.streams.get_highest_resolution(False)

        else:
            video = youtube.streams.filter(res=app.quality.get().split(' ')[0], subtype='mp4', adaptive=True).first()
            if video == None:
                video = youtube.streams.filter(res=app.quality.get().split(' ')[0], adaptive=True).first()
                if video == None:
                    app.in_progress.grid_forget()
                    app.errorMSG.configure(text='Erreur: Qualité sélectionée non disponible !')
                    app.errorMSG.grid(column=1, columnspan=4)
                    return False

        video.download(output_path=app.file_path, filename= 'TEMP' + app.file_name)
        audio = youtube.streams.filter(only_audio=True, file_extension='mp4', adaptive=True).order_by('codecs').first()
        audio.download(output_path=app.file_path, filename= 'TEMP' + app.file_name.split('.')[0] + '.mp3')
        combine_files()
        return True
    else:
        video = youtube.streams.filter(only_audio=True, file_extension='mp4', adaptive=True).order_by('codecs').first()
        video.download(output_path=app.file_path, filename='TEMP' + app.file_name)
        input_aud = ffmpeg.input(app.file_path + '/' + 'TEMP' + app.file_name)
        ffmpeg.output(input_aud.audio, app.file_path + '/' + app.file_name.split('.')[0] + '.mp3').overwrite_output().run(quiet=True)
        os.remove(app.file_path + '/' + 'TEMP' + app.file_name)
        return True

def convert():
    try:
        app.done.grid_forget()
        app.errorMSG.grid_forget()
        app.in_progress.grid_forget()
        if re.search(".*yout.*", app.url.get()):
            if re.search(".*playlist.*", app.url.get()):
                p = Playlist(app.url.get())
                for playlist_video in p.videos:
                    app.file_name = playlist_video.title
                    for k in app.forbidden_chars:
                        app.file_name = app.file_name.replace(k, '')
                    app.file_name += '.mp4'

                    if not odyo_download(playlist_video):
                        return
            else:
                youtube = YouTube(app.url.get())
                app.file_name = youtube.title
                for k in app.forbidden_chars:
                    app.file_name = app.file_name.replace(k, '')
                app.file_name += '.mp4'
                if not odyo_download(youtube):
                    return
        else:
            app.errorMSG.configure(text='Erreur: Lien invalide !')
            app.errorMSG.grid(column=1, columnspan=4)
            return
        app.in_progress.grid_forget()
        app.done.grid(column=1, columnspan=4)
    
    except AgeRestrictedError:
        PushErrorMsg('Erreur: Restriction d\'age !')
    except VideoPrivate:
        PushErrorMsg('Erreur: Vidéo privée !')
    except VideoRegionBlocked:
        PushErrorMsg('Erreur: Vidéo bloquée dans votre région !')
    except Exception as e:
        PushErrorMsg(f'Erreur: Un problème est survenu ! (Error : {type(e).__name__}. More details in errors.log)')
        with open('errors.log', 'a') as file:
            dt = datetime.now()
            file.write(f"{dt.strftime('%d/%m/%Y - %H:%M:%S')} | {type(e).__name__}: {str(e)}\n")
        try:
            os.remove(app.file_path + '/' + 'TEMP' + app.file_name)
            os.remove(app.file_path + '/' + app.file_name.split('.')[0] + '.mp3')
        except:
            return

def PushErrorMsg(m):
    app.in_progress.grid_forget()
    app.errorMSG.configure(text=m)
    app.errorMSG.grid(column=1, columnspan=4)

def combine_files():
    input_vid = ffmpeg.input(app.file_path + '/' + 'TEMP' + app.file_name)
    input_aud = ffmpeg.input(app.file_path + '/' + 'TEMP' + app.file_name.split('.')[0] + '.mp3')
    ffmpeg.concat(input_vid, input_aud, v=1, a=1, unsafe= True)
    ffmpeg.output(input_vid.video, input_aud.audio, app.file_path + '/' + app.file_name, codec='copy').overwrite_output().run(quiet=True)
    os.remove(app.file_path + '/' + 'TEMP' + app.file_name)
    os.remove(app.file_path + '/' + 'TEMP' + app.file_name.split('.')[0] + '.mp3')


def savePath():
    path = askdirectory(initialdir=app.file_path, mustexist=True)
    if not path:
        return
    app.file_path = path
    app.label_path.configure(text='Le fichier sera téléchargé vers: ' + app.file_path)

def checkOS():
    if app.operating_sys == 'Linux':
        app.file_path = str(subprocess.check_output(
            ['xdg-user-dir', 'DESKTOP']).decode('ascii')).rstrip()
        app.label_path.configure(text='Le fichier sera téléchargé vers: ' + app.file_path)

    elif app.operating_sys == 'Windows':
        app.file_path = 'C:/Users/' + app.user + '/Desktop'
        app.label_path.configure(text='Le fichier sera téléchargé vers: ' + app.file_path)

    elif app.operating_sys == 'Darwin':
        app.file_path = '~/Desktop'
        app.label_path.configure(text='Le fichier sera téléchargé vers: ' + app.file_path)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry('500x300')
        self.minsize(500, 300)
        self.title('ODYO Downloader')
        ctk.set_appearance_mode("system")      # Modes: "light", "dark", "system"
        ctk.set_default_color_theme("dark-blue")  # Themes: "blue", "green", "dark-blue"

        self.url = ctk.StringVar()
        self.file_path = str()
        self.file_name = str()
        self.progress = ctk.IntVar()
        self.operating_sys = platform.system()
        self.user = os.getlogin()
        self.forbidden_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*', '.']
        self.ext = ctk.StringVar()
        self.qual = ctk.StringVar()
        self.my_font = ctk.CTkFont("Microsoft Sans Serif")
        self.icon = 'AAABAAIAICAAAAEAIACoEAAAJgAAACAgAAABAAQA6AIAAM4QAAAoAAAAIAAAAEAAAAABACAAAAAAAIAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAB4dXwAeHV8AHh1fAB4dXwAeHV8oHh1fhB4dX80eHV/0Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV/0Hh1fzx4dX4ceHV8rHh1fAB4dXwAeHV8AHh1fAAAAAAAeHV8AHh1fAB4dXwAeHV8LHh1fgR4dX+oeHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX+weHV+FHh1fDR4dXwAeHV8AHh1fAB4dXwAeHV8AHh1fFx4dX7keHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV+/Hh1fGx4dXwAeHV8AHh1fAB4dXwoeHV+5Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV+/Hh1fDR4dXwAeHV8AHh1ffx4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHF//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV+FHh1fAB4dXyUeHV/pHh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Ghlc/xkYXP8gH2D/Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX+0eHV8rHh1ffx4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/xoZXP85OXP/np24/y8va/8YF1v/FhVa/xoZXP8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX4geHV/KHh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//FBNZ/5iYtP+VlLL/DQxU/2Jhj/+ZmLX/Li1r/xgXW/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f0B4dX/MeHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8aGl3/eXmd/ysqaf8lJGT/19bg///////g4Of/VVWG/xYVWv8XFlv/HRxe/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV/1Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8iImP/ERBX/46Nrf////3/+vr4/+zs7/8/Pnb/Hx5g/0tLf/8ZGFz/GBdb/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/xQTWf9GRXv/7+/x//n5+P/+/vz/eXmf/wgHUf9nZpL/+fn4/6urwv9BQHj/HBte/x0cX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8bGl3/JiVl/8fH1f/9/fv////9/6+uxP8VFVr/KShn/9XV3//9/fv//////6yswv8ZGFz/FxZb/xYVWv8cG17/Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/xUUWf+Ih6n////+/////P/Kytf/Jydm/xQUWf+srML////8//z8+v/Z2eL/MzJu/xUVWv+Rka//c3Kb/yEhYv8dHF7/Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//FRRZ/5+fuP//////09Ld/zMybv8NDFT/i4us//39/P/6+vn/7+/x/01Ngf8KCVL/eXmf/////f//////ioqq/xUVWv8WFVr/Ghlc/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8VFFn/o6O8/8vL2P8xMG3/CglS/3l4nv/7+/n/+vr4//v7+f9wb5j/CQlS/1JRg//y8vP//Pz6//Hx8/9JSH7/FxZb/3h3nf82NXD/Gxld/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/xwbXv9PT4H/JSVl/w8OVv93d57/9vb2//v7+f/7+/r/g4Kl/w0MVP8zM2//3Nzk//z8+v////3/jo2t/woKUv9aWon//////7Gxxv8YF1v/HRxf/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hx5f/xIRV/8fHmD/mpq2//v7+v/8/Pr/+vr4/359ov8ODVX/JiZm/8bG1P/+/vz////8/8XE0/8eHWD/JCNk/9TU3v//////tbXJ/xgXXP8dHF//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8aGVz/QkF5/8jI1f/+/vz//Pz6//Pz9P9ubZf/DQtU/ygoZ/+/v8/////8//z8+v/d3eX/Nzdx/w4NVf+iobv////+/6ysw/81NW//Ghld/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/xUUWf+enrj///////7++//o6O3/X1+N/wkJUv82NnD/y8vY/////P/9/fv/4+Pp/0dHfP8ODVX/cnKa/8vL2P9ZWIj/FxZa/xkYXP8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//FRRZ/6Cguf//////xcTU/0FAeP8JCFH/QkJ5/9jY4f////z////8/9zc5P9GRXv/ERBX/0VEev9vbpf/IiJj/xUUWf8dHF//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8XFlr/j4+t/46Orf8cHF//DAtU/11di//k5Or//v77/////f/JyNb/ODhy/xUUWf8fHl//JyZl/xgXXP8cG13/Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8kI2P/DAxU/yUkZP+WlrT/9/f2//7+/P/8/Pr/o6O8/yYlZf8XFlr/Hh1f/x4dX/8dHF7/Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//HRxe/xsaXv9gYI3/1NTe/////f////3/6uru/3Jxmv8XFlv/Ghlc/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/MeHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8WFVr/h4ao//7+/P////z//v78/8DA0P9AP3f/ExJY/x0cXv8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV/0Hh1fyR4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/xQTWf+YmLT//////+np7f99faL/Hh1f/xcWWv8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX84eHV99Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Ghlc/z4+dv+enrj/QUB3/xMSWP8cG17/Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1fhR4dXyMeHV/nHh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Ghpd/xUUWf8ZGFv/Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX+seHV8pHh1fAB4dX3oeHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1fgR4dXwAeHV8AHh1fCB4dX7MeHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX7oeHV8KHh1fAB4dXwAeHV8AHh1fFB4dX7MeHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV+4Hh1fFx4dXwAeHV8AHh1fAB4dXwAeHV8AHh1fCB4dX3oeHV/nHh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV/oHh1ffh4dXwoeHV8AHh1fAB4dXwAAAAAAHh1fAB4dXwAeHV8AHh1fAB4dXyMeHV98Hh1fyB4dX/IeHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/8eHV//Hh1f/x4dX/IeHV/KHh1ffx4dXyUeHV8AHh1fAB4dXwAeHV8AAAAAAB8AAPgHAADgAwAAwAEAAIABAACAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAIABAACAAwAAwAcAAOAfAAD4KAAAACAAAABAAAAAAQAEAAAAAADAAgAAAAAAAAAAAAAAAAAAAAAAAAAAAACJiar/Hh1fwt7e5f9FRHv/Hh1fgRMSWP+ursT/Hh1fAm1slv8eHV///Pz7/zEwbf8eHV8inZy3/8fH1f8IiI1Sqqqqqqqqqqol2IiAiIhaqqqqqqqqqqqqqqWIiIiCqqqqqqqqqqqqqqqqLYiIKqqqqqqqqqqqqqqqqqKIhaqqqqqqqqqqqqqqqqqqWNqqqqpqqqqqqqqqqqqqqq1aqqqmTsZqqqqqqqqqqqqlKqqqpuFpHKqqqqqqqqqqoqqqqqoaw7NKaqqqqqqqqqqqqqqqphu7ykZqqqqqqqqqqqqqqmS7uWm3Rqqqqqqqqqqqqqqvu3bDu3qmqqqqqqqqqqqmG7/Ge7PKGcqqqqqqqqqqpuv8Ybs0absWZqqqqqqqqqZ/xpu7lku7ShyqqqqqqqqqTGm7sWw7sWS3qqqqqqqqqmrru5avu/qjt6qqqqqqqqpPuzls+7PG63yqqqqqqqqm67OWz7s0aflmqqqqqqqqquv0bDuzRkmmqqqqqqqqqqYRppO7/GrGqqqqqqqqqqqqpq67vqqqqqqqqqqqqqqqqmn7s5qqqqqqqqqqqqqqqqYbu/Rqqqqqqqqqqqoqqqqm6zFmqqqqqqqqqqqiWqqqqk5GqqqqqqqqqqqqpdKqqqqmqqqqqqqqqqqqqq2FqqqqqqqqqqqqqqqqqqpYiCqqqqqqqqqqqqqqqqqiiIjSqqqqqqqqqqqqqqqqKIiIiFqqqqqqqqqqqqqqpYiICIiNUqqqqqqqqqqqJdiIgB8AAPgHAADgAwAAwAEAAIABAACAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAIABAACAAwAAwAcAAOAfAAD4'
        self.icon_path = 'C:\\Users\\' + os.getlogin() + '\AppData\Local\Temp\\tmpOdyo.ico'
        
        frm = ctk.CTkFrame(self, fg_color=self.cget("bg"))
        frm.grid()

        with open(self.icon_path, 'wb') as file:
            file.write(base64.b64decode(self.icon))
        self.iconbitmap(self.icon_path)
        os.remove(self.icon_path)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.text = ctk.CTkLabel(frm, text='Lien de la vidéo:', 
                                 font=("Microsoft Sans Serif", 17))
        self.text.grid(column=1, columnspan=4)
        self.text.grid_rowconfigure(1, weight=1)
        self.text.grid_columnconfigure(1, weight=1)

        self.url_textbox = ctk.CTkEntry(frm, width=300, 
                                        text_color='black',
                                        textvariable=self.url, 
                                        fg_color="white",
                                        font=("Microsoft Sans Serif", 14))
        self.url_textbox.focus()
        self.url_textbox.grid(column=1, pady=20, columnspan=2)
        self.url_textbox.grid_rowconfigure(1, weight=1)
        self.url_textbox.grid_columnconfigure(1, weight=1)

        self.L_extension = ['.mp3', '.mp4']
        self.extension = ctk.CTkComboBox(frm, values=self.L_extension,
                         state="readonly", width=70, variable=self.ext, font=("Microsoft Sans Serif", 14))
        self.extension.set(self.L_extension[1])
        self.extension.grid(column=4, row=1)
        self.extension.grid_rowconfigure(1, weight=1)
        self.extension.grid_columnconfigure(1, weight=1)

        self.L_Quality = ['Max', '4320p (8k)', '2160p (4k)', '1440p (2k)', '1080p', '720p', '480p', '360p', '240p', '144p']
        self.quality = ctk.CTkComboBox(frm, values=self.L_Quality,
                                state="readonly", 
                                width=107, variable=self.qual,
                                font=("Microsoft Sans Serif", 14))

        self.quality.set(self.L_Quality[0])
        self.quality.grid(column=3, row=1)
        self.quality.grid_rowconfigure(1, weight=1)
        self.quality.grid_columnconfigure(1, weight=1)

        self.browse = ctk.CTkButton(frm, text='Parcourir',
                                     command=savePath, font=("Microsoft Sans Serif", 15))
        self.browse.grid(column=1, columnspan=4)
        self.browse.grid_rowconfigure(1, weight=1)
        self.browse.grid_columnconfigure(1, weight=1)

        self.label_path = ctk.CTkLabel(
            frm, text='Le fichier sera téléchargé vers: ' + self.file_path,
              font=("Microsoft Sans Serif", 14))
        self.label_path.grid(column=1, columnspan=4, pady=7)
        self.label_path.grid_rowconfigure(1, weight=1)
        self.label_path.grid_columnconfigure(1, weight=1)

        self.convertir = ctk.CTkButton(frm, text='Convertir', 
                                       command=func_thread, font=("Microsoft Sans Serif", 15))
        self.convertir.grid(column=1, columnspan=4)
        self.convertir.grid_rowconfigure(1, weight=1)
        self.convertir.grid_columnconfigure(1, weight=1)

        self.done = ctk.CTkLabel(frm, text='Télechargement Terminé !', text_color='green', font=self.my_font)
        self.done.grid_rowconfigure(1, weight=1)
        self.done.grid_columnconfigure(1, weight=1)

        self.in_progress = ctk.CTkLabel(frm, text='En cours de Téléchargement...', text_color='grey', font=self.my_font)
        self.in_progress.grid_rowconfigure(1, weight=1)
        self.in_progress.grid_columnconfigure(1, weight=1)

        self.errorMSG = ctk.CTkLabel(frm, text_color='red', font=self.my_font)
        self.errorMSG.grid_rowconfigure(1, weight=1)
        self.errorMSG.grid_columnconfigure(1, weight=1)

app = App()
checkOS()
app.mainloop()