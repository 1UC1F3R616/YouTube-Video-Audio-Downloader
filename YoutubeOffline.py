# -*-  coding:utf-8 -*-
from pytube import YouTube, Playlist
import os
import shutil


"""
Audio Codec is WEBM/vorbis.
"""

url = input('Url for video: ')
yt = YouTube(url)
tell = yt.streams.all()
print('Id: 0\tAUDIO ONLY\t--')
for x in yt.streams.all():
	if str(x.resolution)!='None' and str(x.mime_type) == 'video/webm':
		print('Id: '+str(x.itag), '\tResolution: '+str(x.resolution)+'\t'+str(x.filesize//(1024*1024))+' mb')

tag = int(input('Resolution Id: '))
if tag!=0:
    try:
        try:
            shutil.rmtree('videok9')
        except:pass
        os.mkdir('videok9')
        print("Video Download Started.")
        yt.streams.get_by_itag(tag).download('videok9')
        vname = os.listdir('videok9')[0]
        print("Video Download Success.")
    except Exception as e:print(e)

l=[]
for x in yt.streams.all():
		if str(x.mime_type) in ['audio/webm', 'audio/mp4']:
			l.append((str(x.itag), str(x.abr), str(x.mime_type)[6:], str(x.audio_codec), x.default_filename))
for x in l:
	if x[3] in ['vorbis', 'mp4a.40.2']:
		atag = int(x[0])
		aname = x[-1]
		if x[3] == 'vorbis':
			break
else:
	atag = int(l[0][0])

print("Audio Download Started.\n")
yt.streams.get_by_itag(atag).download()
print("Audio Download Success.\n")

if tag!=0:
    try:
        print("Merging using ffmpeg.\n")
        os.system("ffmpeg -i \"videok9/"+vname+"\" -i \""+aname+"\" -ab 192k -r 27 -shortest \""+vname.split('.')[0]+'_.mp4'"\"")
        shutil.rmtree('videok9')
        os.remove(aname)
        print("Success.")
    except Exception as e:
        print(e)
else:
    output = input("Transcode in mp3 from webm/mp4a?: Press 1 else Enter ")
    if output=='1':
        os.system("ffmpeg -i \""+aname+"\" -ab 192 \""+aname.split('.')[0]+"_.mp3"+"\"")
        os.remove(aname)
