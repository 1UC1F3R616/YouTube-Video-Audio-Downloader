# -*-  coding:utf-8 -*-

# Internal Imports
import sys
import random
import subprocess

# Global Colors
reddish = "\033[91m {}\033[00m"
purplelish = "\033[95m {}\033[00m"
cyan = "\033[96m {}\033[00m"
green = "\033[92m {}\033[00m"
blueish = "\033[94m {}\033[00m"

# Global Variables
FORMAT = ''

def welcome_screen():
    preety_text = """
                                ___           ___           ___     
                               /\  \         /\__\         /\__\    
      ___         ___         /::\  \       /:/ _/_       /:/ _/_   
     /|  |       /\__\       /:/\:\  \     /:/ /\__\     /:/ /\__\  
    |:|  |      /:/  /      /:/  \:\  \   /:/ /:/  /    /:/ /:/  /  
    |:|  |     /:/__/      /:/__/ \:\__\ /:/_/:/  /    /:/_/:/  /   
  __|:|__|    /::\  \      \:\  \ /:/  / \:\/:/  /     \:\/:/  /    
 /::::\  \   /:/\:\  \      \:\  /:/  /   \::/__/       \::/__/     
 ~~~~\:\  \  \/__\:\  \      \:\/:/  /     \:\  \        \:\  \     
      \:\__\      \:\__\      \::/  /       \:\__\        \:\__\    
       \/__/       \/__/       \/__/         \/__/         \/__/    
"""

    pick_color = [blueish, purplelish][random.randint(0, 1)]

    print(pick_color .format(preety_text))
    print('\n\n')


def display_error_message(message):
    print(reddish .format('[!] {}\n'.format(message)))
    exit(0)


def help():
    """
    Help Menu
    How to use this script
    """
    pass

def raw_input(input_message):
    something = input(input_message)
    return something


def url_info(url):
    """
    If invalid url then through error
    return: url, platform info, collection type
    platform info is either spotify, yt, yt_music
    collection type is either playlist, single, album
    """
    
    if 'music.youtube.com' in url: platform = 'yt_music'
    elif ('youtu.be' in url) or ('www.youtube.com' in url): platform = 'yt'
    elif 'open.spotify.com' in url: platform = 'spotify'
    else: raise Exception('Failed to identify platform, please check your url')

    return url, platform, 'None'


def yt_commands():
    print('''
    - `yt-dlp -S "height:720" -f "[ext=mp4]+ba[ext=m4a]/b[ext=mp4]" -i url` No better than 720p in mp4
    - `yt-dlp -S "height:720" -i url` mp4 no criteria here
    - `yt-dlp -f "ba" -i url` download best format audio only
    - `yt-dlp -f "ba[ext=mp3]/ba" -i url` mp3 audio format or fallback
    - `yt-dlp --list-formats -i url`list all formats

    - `for f in *.webm ;do ffmpeg -i "$f" -vn -ab 256k -ar 44100 -y "${f%.*}.mp3" -threads 8; done` ffmpeg conversion from other audio formats
    - `for f in *.webm ;do ffmpeg -i "$f" -vn -ab 320k -ar 48000 -y "${f%.*}.mp3" -threads 8; done` ffmpeg conversion from other audio formats
    ''')


def menu():
    if len(sys.argv[1:]) == 0:
        help() # Display help menu if no url and options are passed
        exit(0)
    
    try:
        url, platform, collection_type = url_info(sys.argv[1])
    except Exception as e:
        display_error_message(e)

    if platform == 'spotify': # spotify supports mp3 downloads only as of now
        # it's safe to pass any argument here. @1UC1F3R616
        arg1 = url
        if len(sys.argv[1:]) >= 2:
            arg2 = sys.argv[2] # mp3/m4a/flac/opus/ogg/wav
            if arg2 not in ['mp3', 'm4a', 'flac', 'opus', 'ogg', 'wav']:
                arg2 = 'mp3'
            if len(sys.argv[1:]) == 3:
                arg3 = sys.argv[3] # location for downloading the content
            else: arg3 = '.'
        else:
            arg2 = 'mp3'
            arg3= '.'
        try:
            result = subprocess.Popen(['spotdl', arg1, '--output-format', arg2, '--dt', '4', '--st', '8'], stdout=sys.stdout, stderr=sys.stderr, cwd=arg3)
        except Exception as e:
            display_error_message(e)
    elif platform in ['yt', 'yt_music']:
        yt_commands()
            

        




if  __name__ == '__main__':
    welcome_screen()
    menu()
