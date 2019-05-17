# -*-  coding:utf-8 -*-

# Imports
from pytube import YouTube, Playlist
import os
import shutil
from pyfiglet import figlet_format as ff
from random import randint


# Function to Download a single video
def single(url):
    yt = YouTube(url)
    print("[-] Now Downloading %s\n" % yt.title)
    tell = yt.streams.all()
    print('[+] Id: 0\t\tAUDIO ONLY')
    for x in yt.streams.all():
            if str(x.resolution)!='None' and str(x.mime_type) == 'video/webm':
                    print('[+] Id: '+str(x.itag), '\tResolution: '+str(x.resolution)+'\t'+str(x.filesize//(1024*1024))+' mb')

    tag = int(input('[+] Resolution Id: '))
    if tag!=0:
        try:
            try:shutil.rmtree('videok9')
            except:pass
            os.mkdir('videok9')
            print('[-] Video Download Started: ',yt.title)
            yt.streams.get_by_itag(tag).download('videok9')
            vname = os.listdir('videok9')[0]
        except Exception as e:print('[-]', e)

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

    print("[-] Audio Download Started.\n")
    yt.streams.get_by_itag(atag).download()

    if tag!=0:
        try:
            print("[-] Merging using ffmpeg.\n")
            os.system("ffmpeg -i \"videok9/"+vname+"\" -i \""+aname+"\" -ab 192k -r 27 -shortest \""+vname.split('.')[0]+'_.mp4'"\"")
            shutil.rmtree('videok9')
            os.remove(aname)
            print('            [S][U][C][C][E][S][S]            ')
        except Exception as e:
            print(e)
    else:
        output = input("[+] Transcode in mp3 from webm/mp4a?: Press 1 else Enter ")
        if output=='1':
            os.system("ffmpeg -i \""+aname+"\" -ab 192 \""+aname.split('.')[0]+"_.mp3"+"\"")
            os.remove(aname)
        print('            [S][U][C][C][E][S][S]            ')


# Playlist Download
def playlist(url):
    pl = Playlist(url)
    pl.populate_video_urls() # We need t populate it otherwise video_urls will give an empty list.
    videos = pl.video_urls
    #print(videos)
    #print('second')
    tag = int(input("""
        >> Enter 0 to download Audio only.
        >> Enter Video-Resolution ID to be downloaded.
        >> Ex. '247' without quotes for 720p res.

        
        Available Resolutions\n:
        [+] ID: 248     1080p
        [+] ID: 247     720p
        [+] ID: 244     480p
        [+] ID: 243     360p
        [+] ID: 242     240p
        [+] ID: 278     144p\n
        """))
    print('>>> Script is executed Successfully.')
    print('>>> Give a star if it helps you. It will encorage me :)')
    print('>>> ffmpeg console will appear, ignore it. Do not close or else merge will fail.')
    if tag != 0:
        for iurl in videos:
            yt = YouTube(iurl)
            try:
                try:shutil.rmtree('videok9')
                except:pass
                os.mkdir('videok9')
                yt.streams.get_by_itag(tag).download('videok9')
                print("[-] Success: ", yt.title)
                vname = os.listdir('videok9')[0]
                make_needed = True
            except Exception as e:
                make_needed = False
                if str(e) == "'NoneType' object has no attribute 'download'":
                    print("[*] Format decreased for: ",yt.title)
                    try:
                        yt.streams.filter(progressive=True).order_by('resolution').desc().first().download()
                        print("[-] success: ", yt.title)
                    except:
                        print('[*]', yt.title, ' ::is skipped fully. Please download using command line.')
                        
            if make_needed: #not needed means audio and video are present already.
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

                yt.streams.get_by_itag(atag).download()
                
                try:
                    os.system("ffmpeg -i \"videok9/"+vname+"\" -i \""+aname+"\" -ab 160k -r 27 -shortest \""+vname.split('.')[0]+'_.mp4'"\"")
                    shutil.rmtree('videok9')
                    os.remove(aname)
                    print("            [S][U][C][C][E][S][S]            ")
                except Exception as e:
                    print('[*]', e)
                    print("[*] Make sure ffmpeg is added in Environment Variable.")
            else:pass
                    
    elif tag == 0:
            output = input("[+] Transcode in mp3 from webm/mp4a?: Press 1 else Enter ")
            for iurl in videos:
                aname = yt.streams.filter(only_audio=True).first().default_filename
                yt = YouTube(iurl)
                print('[-] success: ',yt.title)
                yt.streams.filter(only_audio=True).first().download()
                if output=='1':
                    os.system("ffmpeg -i \""+aname+"\" -ab 160k \""+aname.split('.')[0]+"_.mp3"+"\"")
                    os.remove(aname)
    else:
            print('[*] Enter correct choice like 243')
            playlist()


if __name__ == "__main__":

    # Wanna Be Cool
    print(ff('YToff' ,font=['block', 'isometric1', 'isometric2'][randint(0,2)]))

    url = input('[+] Url for Video/Playlist: ')

    # Decide if playlist or single track
    try:
        if 'https://www.youtube.com/playlist?' in url:
            playlist(url)
        else:
            single(url)
    except Exception as e:
        print(e, '\n[*] Give YouTube Video or Playlist link.')

    input('            [F][U][L][L][][S][U][C][C][E][S][S]            ')

