from pytube import YouTube
import os

url = input('Lien de la vidéo: ')
youtube = YouTube(url)
video = youtube.streams.get_by_itag(140) #140 correspond au .mp4 audio suelement en 128kb/s
outfile = video.download('/home/puff/Vidéos')

#rename fichier de sortie
base, ext = os.path.splitext(outfile)
newfile = base + '.mp3'
os.rename(outfile, newfile)